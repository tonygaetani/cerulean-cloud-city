#!/usr/bin/env bash
set -euo pipefail

IFS=
# http://stackoverflow.com/a/246128/6554
SOURCE="${BASH_SOURCE[0]}"
# resolve $SOURCE until the file is no longer a symlink
while [ -h "$SOURCE" ]; do
        DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
        SOURCE="$(readlink "$SOURCE")"
        # if $SOURCE was a relative symlink, we need to resolve it relative to the
        # path where the symlink file was located
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

IFS=$'\n\t'

function help() {
  echo -e "usage:"
  echo -e "\tbash main.bash"
  echo -e "required environment:"
  echo -e "\tGIT_REPO or GIT_DIR"
  echo -e "\tOUTPUT_DIR"
  echo -e "\tSOUNDCLOUD_CLIENT_ID"
  echo -e "\tSOUNDCLOUD_CLIENT_SECRET"
  echo -e "\tSOUNDCLOUD_USERNAME"
  echo -e "\tSOUNDCLOUD_PASSWORD"
  echo -e "optional environment:"
  echo -e "\tDEBUG"
  echo -e "\tVERBOSE"
}

if [[ "${1-}" == "help" ]]; then
  help
  exit 0
fi

#
# no standard output unless in debug mode
#
if [[ -n "${DEBUG-}" && ! "${DEBUG-}" =~ [Ff]alse ]]; then
  export __CCC_DEBUG__="True"
else
	exec 1> /dev/null 2>&1
fi

#
# show commands in verbose mode
#
if [[ -n "${VERBOSE-}" ]]; then
	set -x
fi

#
# set up required environment variables
#
if [[ -z "${GIT_REPO-}" && -z "${GIT_DIR-}" ]]; then
  help
	exit 100
fi

if [[ -z "${OUTPUT_DIR-}" ]]; then
  help
  exit 101
fi

if [[ -z "${SOUNDCLOUD_CLIENT_ID-}" ]]; then
  help
  exit 102
fi

if [[ -z "${SOUNDCLOUD_CLIENT_SECRET-}" ]]; then
  help
  exit 103
fi

if [[ -z "${SOUNDCLOUD_USERNAME-}" ]]; then
  help
  exit 104
fi

if [[ -z "${SOUNDCLOUD_PASSWORD-}" ]]; then
  help
  exit 105
fi

#
# project root used by python scripts
#
export PROJECT_ROOT="${DIR}"


#
# create a temp directory and clean it with a trap
#
if [[ -z "${GIT_DIR-}" && -n "${GIT_REPO}" ]]; then
  GIT_DIR=$(mktemp -d tmp$(date +%s))
  trap 'rm -rf "${GIT_DIR}"' INT TERM EXIT

  #
  # clone git repo to temp dir
  #
  git clone "${GIT_REPO}" "${GIT_DIR}/"
else
  #
  # the python scripts use GIT_REPO not git dir
  #
  export GIT_REPO="${GIT_DIR}"
fi

#
# sync with soundcloud
#
GIT_REPO="${GIT_DIR}" env python scupload/scupload.py

mkdir -p "${OUTPUT_DIR}"
find "${OUTPUT_DIR}" | \
grep --invert-match \.git | \
xargs rm -rf || true

#
# generate web pages
#
GIT_REPO="${GIT_DIR}" BUILD_DIR="${OUTPUT_DIR}" env python cccmake/cccmake.py










