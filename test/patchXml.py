#! /bin/env python2.4

import os
import sys
from xml.dom.minidom import parse

name = []
rads = []
dedx = []

# parse data file
data = open('parameters')
lines = data.readlines()
for line in lines:
  tokens = line.split()
  name.append( tokens[0] )
  rads.append( float(tokens[6]) )
  dedx.append( float(tokens[9]) )

# check for merged Z+ Z- endcaps
if len(name) == 27:
  # pixel disk
  name[15:15] = name[13:15]
  rads[15:15] = rads[13:15]
  dedx[15:15] = dedx[13:15]
  # TID
  name[20:20] = name[17:20]
  rads[20:20] = rads[17:20]
  dedx[20:20] = dedx[17:20]
  # TEC
  name[32:32] = name[23:32]
  rads[32:32] = rads[23:32]
  dedx[32:32] = dedx[23:32]
  
# parse xml file
if 'CMSSW_RELEASE_BASE' not in os.environ:
  print 'please define the CMSSW environment with "eval `scramv1 runtime -sh`"'
  sys.exit(1)

relative_xml = 'Geometry/TrackerRecoData/data/trackerRecoMaterial.xml'
release_xml = os.environ['CMSSW_RELEASE_BASE'] + '/src/' + relative_xml
updated_xml = os.environ['CMSSW_BASE']         + '/src/' + relative_xml
  
if os.path.exists(updated_xml):
  dom = parse(updated_xml)
  sys.stderr.write( 'Update from working area XML\n' )
else:
  dom = parse(release_xml)
  sys.stderr.write( 'Update from release XML\n' )
  
layers = dom.getElementsByTagName('SpecPar')

for layer in layers:
  sys.stderr.write( '%-36s\t<--  %s\n' % (layer.getAttribute('name'), name.pop(0)) )
  parameters = layer.getElementsByTagName('Parameter')
  for parameter in parameters:
    if parameter.getAttribute('name') == u'TrackerRadLength':
      sys.stderr.write( '\t%-20s%10f\t-->%10f\n' % (parameter.getAttribute('name'), float(parameter.getAttribute('value')), rads[0] ) )
      parameter.setAttribute('value', str(rads.pop(0)))
    if parameter.getAttribute('name') == u'TrackerXi':
      sys.stderr.write( '\t%-20s%10f\t-->%10f\n' % (parameter.getAttribute('name'), float(parameter.getAttribute('value')), dedx[0] ) )
      parameter.setAttribute('value', str(dedx.pop(0)))

print dom.toxml()
