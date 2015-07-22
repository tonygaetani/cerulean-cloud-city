#!/usr/bin/env python

import os
project_root = os.environ['PROJECT_ROOT']

import sys
sys.path.append( "{0}/cerulean-cloud-city".format(project_root))
from ceruleancc import *

import soundcloud

class CccSoundcloudUserException(Exception):
    pass

def getid(track_name):
    # get the current tracks on soundcloud
    soundcloud_tracks = client.get("/users/{0}/tracks".format(band.metadata['soundcloud_userid']))
    for track in soundcloud_tracks:
        if str(track.title) == track_name:
            return str(track.id)
    raise CccSoundcloudUserException

input_directory = os.environ['GIT_REPO']
soundcloud_client_id = os.environ['SOUNDCLOUD_CLIENT_ID']
soundcloud_client_secret = os.environ['SOUNDCLOUD_CLIENT_SECRET']
soundcloud_username = os.environ['SOUNDCLOUD_USERNAME']
soundcloud_password = os.environ['SOUNDCLOUD_PASSWORD']

# build a band object from the input dir
band = CccBand(input_directory)

# get a soundcloud client
client = soundcloud.Client(
    client_id=soundcloud_client_id,
    client_secret=soundcloud_client_secret,
    username=soundcloud_username,
    password=soundcloud_password,
)