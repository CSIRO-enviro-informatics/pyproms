import datetime
from pyproms import *

# Example Agents, could be people or Organisations
ag = ProvAgent("Agent Orange")
agx = ProvAgent("Agent X")

# A ReportingSystem (Agent subclass)
# This is the system that actually generates the Reports
rs = PromsReportingSystem('Workflow System Z')

# The single Activity, as Basic Reports only allow 1
startedAtTime = datetime.datetime.strptime('2014-06-25T12:13:14', '%Y-%m-%dT%H:%M:%S')
endedAtTime = datetime.datetime.strptime('2014-06-25T12:13:24', '%Y-%m-%dT%H:%M:%S')
report_activity = ProvActivity('Test Activity',
                               startedAtTime,
                               endedAtTime,
                               wasAssociatedWith=agx,
                               comment='A test Activity')

# The Report
r = PromsBasicReport('Test Basic Report PyPROMS',
                     rs,  # this is the Reporting System
                     'report-71',  # this could be anything that the Reporting System uses to keep track of Reports
                     report_activity,
                     comment='This is an example Basic Report')

# Save the report
report_file = 'example_basic_report.ttl'
with open(report_file, 'w') as f:
    f.write((r.get_graph().serialize(format='n3')).decode('UTF-8'))

 #print the report, just for testing
print open(report_file).read()

# Send (POST) the Report to a PROMS Server instance
#pr = Reporter().post('http://some-proms-server.org.au/reportingsystem/workflow_system_z/report/', r)
