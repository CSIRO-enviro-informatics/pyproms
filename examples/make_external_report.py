from datetime import datetime
from pyproms import *

# example Agents, could be people or Organisations
ag = ProvAgent("Agent Orange")
agx = ProvAgent("Agent X")

# a ReportingSystem (Agent subclass)
# this is the system that actually generates the Reports
rs = PromsReportingSystem('Workflow System Z')

# a very basic input Entity defined by a URI only
entity_used_01 = ProvEntity('Dataset 12', uri='http://pid.geoscience.gov.au/dataset/12')

# an input Entity with full details
entity_used_02 = ProvEntity('Input 02',
                            comment='The Entity, 02',
                            wasAttributedTo=ag)

# the sole output Entity
entity_generated_03 = ProvEntity('Output Data',
                                 uri='http://web3-wron:8080/water/thredds/somefile.nc',
                                 comment='The Entity, 03',
                                 wasAttributedTo=ag)

# the single Activity, as External Reports only allow 1
startedAtTime = datetime.strptime('2014-06-25T12:13:14', '%Y-%m-%dT%H:%M:%S')
endedAtTime = datetime.strptime('2014-06-25T12:13:24', '%Y-%m-%dT%H:%M:%S')
report_activity = ProvActivity('Test Activity',
                               startedAtTime,
                               endedAtTime,
                               wasAssociatedWith=agx,
                               comment='A test Activity',
                               used_entities=[entity_used_01, entity_used_02],
                               generated_entities=[entity_generated_03])

# make the Report
r = PromsExternalReport('Test External Report PyPROMS',
                        rs,  # this is the Reporting System
                        'report-71',  # this could be anything that the Reporting System uses to keep track of Reports
                        report_activity,
                        generatedAtTime=datetime.strptime('2014-06-25T12:13:34', '%Y-%m-%dT%H:%M:%S'),
                        comment='This is an example Basic Report')

# Save the report
report_file = 'example_report_external.ttl'
with open(report_file, 'w') as f:
    f.write((r.get_graph().serialize(format='n3')).decode('UTF-8'))

# print the report, just for testing
print(open(report_file).read())

# send (POST) the Report to a PROMS Server instance
#pr = Reporter().post('http://some-proms-server.org.au/reportingsystem/workflow_system_z/report/', r)
