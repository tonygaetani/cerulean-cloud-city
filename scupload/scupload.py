#!/usr/bin/env python

import os
project_root = os.environ['PROJECT_ROOT']

import sys
sys.path.append( "{0}/cerulean-cloud-city".format(project_root))
from ceruleancc import *

import soundcloud

# globals from environment
input_directory = os.environ['GIT_REPO']
soundcloud_client_id = os.environ['SOUNDCLOUD_CLIENT_ID']
soundcloud_client_secret = os.environ['SOUNDCLOUD_CLIENT_SECRET']
soundcloud_username = os.environ['SOUNDCLOUD_USERNAME']
soundcloud_password = os.environ['SOUNDCLOUD_PASSWORD']
__CCC_DEBUG__ = os.getenv('__CCC_DEBUG__', False)

# build a band object from the input dir
if __CCC_DEBUG__: sys.stdout.write("loading band from path {0}\n".format(input_directory))
band = CccBand(input_directory)

# get a soundcloud client
client = soundcloud.Client(
    client_id=soundcloud_client_id,
    client_secret=soundcloud_client_secret,
    username=soundcloud_username,
    password=soundcloud_password,
)

# get the current tracks on soundcloud
if __CCC_DEBUG__: sys.stdout.write("getting tracks for soundcloud user {0}\n".format(band.metadata['soundcloud_userid']))
soundcloud_tracks = client.get("/users/{0}/tracks".format(band.metadata['soundcloud_userid']))
soundcloud_track_to_id = {}
for track in soundcloud_tracks:
    soundcloud_track_to_id[str(track.title)] = str(track.id)
    if __CCC_DEBUG__: sys.stdout.write("found track {0} (id: {1})\n".format(str(track.title), str(track.id)))

# upload the sounds to soundcloud
for album in band.albums:
    for track in album.tracks:
        if track.name not in soundcloud_track_to_id.keys():
            if __CCC_DEBUG__: sys.stdout.write("uploading {0} from {1}\n".format(track.name, track.path))
            client.post('/tracks', track={
                'title': track.name,
                'asset_data': open(track.path, 'rb')
            })
        else:
            # this track already exists
            # has the sha1sum changed?
            if __CCC_DEBUG__: sys.stdout.write("won't upload track {0} (already exists)\n".format(track.name))
