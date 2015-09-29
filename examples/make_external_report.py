import datetime
from pyproms import *

# Example Agents, could be people or Organisations
ag = ProvAgent("Agent Orange")
agx = ProvAgent("Agent X")

# A ReportingSystem (Agent subclass)
# This is the system that actually generates the Reports
rs = PromsReportingSystem('Workflow System Z')

# A very basic input Entity defined by a URI only
entity_used_01 = ProvEntity('', uri='http://web3-wron:8080/water/thredds/fileServer/Awra/AwraL/355/Daily/Ss/2012/20120923_Ss')

# An input Entity with full details
entity_used_02 = ProvEntity('Input 02',
                            comment='The Entity, 02',
                            created=datetime.datetime.strptime('2014-06-25T12:00:02', '%Y-%m-%dT%H:%M:%S'),
                            wasAttributedTo=ag,
                            licence='http://creativecommons.org/licenses/by/4.0/')

# The sole output Entity
entity_generated_03 = ProvEntity('Output Data',
                                 uri='http://web3-wron:8080/water/thredds/somefile.nc',
                                 comment='The Entity, 03',
                                 wasAttributedTo=ag,
                                 creator=agx,
                                 created=datetime.datetime.strptime('2014-06-25T12:13:01', '%Y-%m-%dT%H:%M:%S'),
                                 licence='http://creativecommons.org/licenses/by/4.0/',
                                 downloadURL='http://web3-wron:8080/water/thredds/somefile.nc')

# The single Activity, as External Reports only allow 1
startedAtTime = datetime.datetime.strptime('2014-06-25T12:13:14', '%Y-%m-%dT%H:%M:%S')
endedAtTime = datetime.datetime.strptime('2014-06-25T12:13:24', '%Y-%m-%dT%H:%M:%S')
report_activity = ProvActivity('Test Activity',
                               startedAtTime,
                               endedAtTime,
                               wasAssociatedWith=agx,
                               comment='A test Activity',
                               used_entities=[entity_used_01, entity_used_02],
                               generated_entities=[entity_generated_03])

# The Report
r = PromsExternalReport('Test External Report PyPROMS',
                        rs,  # this is the Reporting System
                        'report-71',  # this could be anything that the Reporting System uses to keep track of Reports
                        report_activity,
                        comment='This is an example Basic Report')

# Save the report
report_file = 'example_external_report.ttl'
with open(report_file, 'w') as f:
    f.write((r.get_graph().serialize(format='n3')).decode('UTF-8'))

 #print the report, just for testing
print open(report_file).read()

# Send (POST) the Report to a PROMS Server instance
#pr = Reporter().post('http://some-proms-server.org.au/reportingsystem/workflow_system_z/report/', r)
