#! /bin/env python2.4

import os
import sys
from xml.dom.minidom import parse

rads = []
dedx = []

# parse data file
data = open('parameters')
lines = data.readlines()
for line in lines:
  tokens = line.split()
  rads.append( float(tokens[6]) )
  dedx.append( float(tokens[9]) )

# parse xml file
if 'CMSSW_RELEASE_BASE' not in os.environ:
  print 'please define the CMSSW environment with "eval `scramv1 runtime -sh`"'
  sys.exit(1)

dom = parse(os.environ['CMSSW_RELEASE_BASE'] + '/src/Geometry/TrackerRecoData/data/trackerRecoMaterial.xml')
layers = dom.getElementsByTagName('SpecPar')

for layer in layers:
  parameters = layer.getElementsByTagName('Parameter')
  for parameter in parameters:
    if parameter.getAttribute('name') == u'TrackerRadLength':
      parameter.setAttribute('value', str(rads.pop(0)))
    if parameter.getAttribute('name') == u'TrackerXi':
      parameter.setAttribute('value', str(dedx.pop(0)))

print dom.toxml()
