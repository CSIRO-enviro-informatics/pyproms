"""
This file creates an example Report (External) with the following details:

    1 x Report class object
    1 x Activity class object
    2 x input Entity class object
        1. an Entity defined by URI only
        2. a locally-defined Entity
    1 x output Entity class object
    2 x Agent Entity class objects
        1. A person agent
        2. A system agent
"""
# TODO: complete above layout
# TODO: move to examples
# TODO: provide other examples
# TODO: make tests check examples
# TODO: increment pip versions & republish
# TODO: email Matt Pagett & Ed re AHRCC process being changed now use pyproms
from datetime import datetime
from pyproms import ProvActivity, ProvAgent, ProvEntity
from pyproms.proms_entity import PromsEntity
from pyproms.proms_activity import PromsActivity
from pyproms.proms_reportingsystem import PromsReportingSystem
from pyproms.proms_report import PromsReport, ReportType



'''
PROMS RS
'''
rs1 = PromsReportingSystem('CSIRO Reporting System 2314',
                          uri='http://pid.csiro.au/agent/rs-2314',
                          comment='AHRCC Ocean Colour satellite ground station receiver processing trigger agent')
#print rs1.serialize_graph()

'''
PROV Entity
'''
e1 = ProvEntity('Test PROV Entity',
               uri='http://go.to#wrtw',
               downloadURL='http://example.com/4')
e1.set_uri('http://example.org/id/dataset/44')
e1.set_downloadURL('http://other.com')
#print e1.serialize_graph(format="turtle")


'''
PROMS Entity
'''
e2 = PromsEntity('Test PROMS Entity',
                 uri='http://go.to#wrtw',
                 downloadURL='http://example.com/4')
e2.set_uri('http://example.org/id/dataset/45')
e2.set_downloadURL('http://other.com')
#print e2.serialize_graph(format="turtle")


'''
PROV Entity
'''
e3 = ProvEntity('Test PROV Entity #2')
#print e1.serialize_graph(format="turtle")

'''
PROV Agent
'''
ag1 = ProvAgent('Agent Nick',
                name='Nicholas Car',
                mbox='nicholas.car@csiro.au')
#print ag1.serialize_graph(format="turtle")

'''
PROV Activity
'''
a1 = ProvActivity('Test PROV Activity',
                  datetime.strptime('2015-01-01T12:00:00', '%Y-%m-%dT%H:%M:%S'),
                  datetime.strptime('2015-01-01T14:00:00', '%Y-%m-%dT%H:%M:%S'),
                  uri=None,
                  wasAssociatedWith=ag1,
                  used_entities=[e1, e2])
#print a1.serialize_graph(format="turtle")

'''
PROV Activity
'''
a1b = ProvActivity('Test PROV Activity B',
                  datetime.strptime('2015-01-01T14:01:00', '%Y-%m-%dT%H:%M:%S'),
                  datetime.strptime('2015-01-01T15:00:00', '%Y-%m-%dT%H:%M:%S'),
                  uri=None,
                  wasAssociatedWith=ag1,
                  wasInformedBy=a1,
                  used_entities=[e1, e2])
#print a1b.serialize_graph(format="turtle")

'''
PROMS Activity -- not working due to recursion issue (Nick, 16/02/2015
'''
'''
a2 = PromsActivity('Test PROMS Activity',
                  uri=None,
                  wasAssociatedWith=ag1,
                  used_entities=[e1, e2],
                  #wasInformedBy=a1,
                  #namedActivityUri='http://www.namedactivity.com/activity/34'
                  )
print a2.serialize_graph(format="turtle")
#'''

r1 = PromsReport('Test Report',
                ReportType.External,
                rs1,
                'abc123-def456',
                a1,
                a1b,
                'Test Report generation from pyproms')
print r1.serialize_graph()
