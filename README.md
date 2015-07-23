cerulean cloud city
===================
a framework for organizing, storing and sharing your music

github repository for music
===========================
the data model of your music

all of your music lives in this repository in a structured format

contents
--------
metadata.yaml - yaml file describing the data of the band

 - albums folder  - all albums of the band

  - album folder - all data for an album, the folder name is the name of the album

   - 000song.mp3 - mp3 song

   - metadata.yaml - yaml file describing the data of the album

   - album.zip


directory structure
-------------------
/band

 -  /album 1

  -    track1.mp3

  -     ...

  -     trackn.mp3

 -   /album n


github pages repository
=======================
the front end for your music

the landing page lists all band and album data from the music repository

each album has its own webpage

each album has a zip download link

each track has a download link and a soundcloud embed


the main.bash program
====================
ties all of the tools in this repository together. the output comes in two 
different forms: a github pages-ready website folder and all new tracks 
uploaded to soundcloud.

requirements
------------
bash

git

python 2.7

soundcloud api for python


enironment
----------
OUTPUT_DIR (required)

GIT_REPO or GIT_DIR (one is required)

 - one of these two is used as the cerulean cloud city git repository for music

 - GIT_DIR a local directory (takes priority)

 - GIT_REPO will be cloned into a temp dir and deleted (must be set exclusively) 


SOUNDCLOUD_ACCESS_KEY_ID (required)

SOUNCLOUD_SECRET_ACCESS_KEY (required)

SOUNDCLOUD_USERNAME (required)

SOUNDCLOUD_PASSWORD (required)

DEBUG

VERBOSE


usage
-----
```
bash main.bash
```

return codes
------------

0 - success

1 - failure (unknown)

100+ - failure (known)

100 - missing environment GIT_REPO

101 - missing environment OUTPUT_DIR

102 - missing environment SOUNDCLOUD_CLIENT_ID

103 - missing environment SOUNCLOUD_SECRET_ACCESS_KEY

104 - missing environment SOUNDCLOUD_USERNAME

105 - missing environment SOUNDCLOUD_PASSWORD


the scupload program
====================
uploads the latest content from a cerulean cloud city git repository for music 
to soundcloud. the repository must be a valid cerulean cloud city git 
repository for music.

requirements
------------
python 2.7

soundcloud api for python


enironment
----------
PROJECT_ROOT

GIT_REPO

SOUNDCLOUD_ACCESS_KEY_ID

SOUNCLOUD_SECRET_ACCESS_KEY

SOUNDCLOUD_USERNAME

SOUNDCLOUD_PASSWORD

__CCC_DEBUG__


usage
-----
```
python scupload.py
```

return codes
------------
0 - success

1 - failure

the cccmake program
====================
builds and updates a website based on the latest content from a cerulean cloud 
city git repository for music. the repository must be a valid cerulean cloud 
ciy github repository for music.

requirements
------------
python 2.7

enironment
----------
PROJECT_ROOT

GIT_REPO

BUILD_DIR

usage
-----
```
python cccmake.py
```

return codes
------------
0 - success

1 - failure

the ceruleancc library
====================
provides classes that describe a cerulean cloud city git repository for music

requirements
------------
python 2.7

usage
-----
see tests/ccctest.py and main.bash for examples

the sctrackid library
====================
retrieves a trackid from soundcloud

requirements
------------
python 2.7

enironment
----------
PROJECT_ROOT

GIT_REPO

SOUNDCLOUD_ACCESS_KEY_ID

SOUNCLOUD_SECRET_ACCESS_KEY

SOUNDCLOUD_USERNAME

SOUNDCLOUD_PASSWORD


usage
-----
see tests/sctrackidtest.py














