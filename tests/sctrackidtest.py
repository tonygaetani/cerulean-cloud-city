#!/usr/bin/env python
import os
project_root = os.environ['PROJECT_ROOT']

import sys
sys.path.append( "{0}/cerulean-cloud-city".format(project_root))
sys.path.append( "{0}/sctrackid".format(project_root))
from ceruleancc import CccBand
from sctrackid import *

import uuid

input_directory = os.environ['GIT_REPO']

# test normal usage
band = CccBand(input_directory)
for album in band.albums:
  for track in album.tracks:
    print getid(track.name)

# test failure
try:
  print getid(str(uuid.uuid1()))
except CccSoundcloudUserException:
  print "success"