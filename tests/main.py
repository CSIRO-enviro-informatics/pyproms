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
# TODO: re-implement in Git
# TODO: complete above layout
# TODO: move to examples
# TODO: provide other examples
# TODO: make tests check examples
# TODO: increment pip versions & reputh
# TODO: email Matt Paget & Ed re AHRCC process being changed now use pyproms
from pyproms.entity import Entity

e = Entity('PROMS',
           'Test Entity',
           uri='http://go.to#wrtw',
           downloadURL='http://example.com/4')
#e.set_uri('http://example.org/id/dataset/44')
e.set_downloadURL('http://other.com')

print e.serialize_graph('turtle')