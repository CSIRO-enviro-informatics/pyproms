import datetime
from pyproms import *

#a very basic Entity defined by a URI only
entity_used_01 = Entity('http://web3-wron:8080/water/thredds/fileServer/Awra/AwraL/355/Daily/Ss/2012/20120923_Ss')

entity_used_02 = Entity(None,
                        'Entity 02',
                        'The Entity, 02',
                        datetime.datetime.strptime('2014-06-25T12:00:02', '%Y-%m-%dT%H:%M:%S'),
                        'http://pid.csiro.au/person/car587',
                        'http://creativecommons.org/licenses/by/4.0/',
                        ConfidentialityStatus.PublicDomain,
                        None,
                        None)

entity_generated_03 = Entity(None,
                             'Entity 03',
                             'The Entity, 03',
                             datetime.datetime.strptime('2014-06-25T12:13:01', '%Y-%m-%dT%H:%M:%S'),
                             'http://pid.csiro.au/person/car587',
                             'http://creativecommons.org/licenses/by/4.0/',
                             ConfidentialityStatus.PublicDomain,
                             None,
                             'http://web3-wron:8080/water/thredds/somefile.nc')

#make the Activity
startedAtTime = datetime.datetime.strptime('2014-06-25T12:13:14', '%Y-%m-%dT%H:%M:%S')
endedAtTime = datetime.datetime.strptime('2014-06-25T12:13:24', '%Y-%m-%dT%H:%M:%S')
report_activity = Activity(None,
                           'Test Activity',
                           'A tests Activity',
                           'http://pid.csiro.au/person/car587',
                           startedAtTime, endedAtTime,
                           [entity_used_01, entity_used_02],
                           [entity_generated_03])

#make the Report
r = Report(None,
           ReportType.External,
           'Test Basic Report PyPROMS',
           'A tests Basic Report',
           report_activity,
           startedAtTime,
           report_activity,
           endedAtTime)

#save the report
with open("basic_report.ttl", 'w') as f:
    f.write((r.get_graph().serialize(format='n3')).decode('UTF-8'))

#print the report
print open("basic_report.ttl").read()

#make the reporter
#pr = Reporter()
#pr.post('http://butterfree-bu.nexus.csiro.au:8000/reportingsystem/demosys/report/', r)
