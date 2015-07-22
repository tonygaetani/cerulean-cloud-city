#!/usr/bin/env python
import os
project_root = os.environ['PROJECT_ROOT']

import sys
sys.path.append( "{0}/cerulean-cloud-city".format(project_root))
from ceruleancc import CccBand

band = CccBand('/Users/tonygaetani/SWEngineering/cerulean')
print str(band)
