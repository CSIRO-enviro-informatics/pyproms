import datetime
from rdflib import URIRef, Namespace, Graph, Literal, BNode, compare, serializer
from rdflib.namespace import RDF
from pyproms import activity


def test_activity_basic():
    activity_uri = 'http://promsns.org/demo/abc-123'
    title = 'Test Activity'
    description = 'A tests Activity'
    wasAttributedTo = 'http://example.com/person/nicholas.car'
    startedAtTime = datetime.datetime.strptime('2014-01-01T12:13:14',
                                               '%Y-%m-%dT%H:%M:%S')
    endedAtTime = datetime.datetime.strptime('2014-01-01T12:13:24',
                                               '%Y-%m-%dT%H:%M:%S')
    used_entities = None
    generated_entities = None

    #create an Activity by hand for comparison and make graph
    XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
    DC = Namespace('http://purl.org/dc/elements/1.1/')

    g = Graph()
    PROV = Namespace('http://www.w3.org/ns/prov#')
    g.add((URIRef(activity_uri), RDF.type, PROV.Activity))
    g.add((URIRef(activity_uri), DC.title, Literal(title)))
    g.add((URIRef(activity_uri), DC.description, Literal(description)))
    g.add((URIRef(activity_uri), PROV.wasAttributedTo, URIRef(wasAttributedTo)))
    g.add((URIRef(activity_uri), PROV.startedAtTime, Literal(
        startedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))
    g.add((URIRef(activity_uri), PROV.endedAtTime, Literal(
        endedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))

    #instantiate Activity & get_graph
    a = activity.Activity(activity_uri, title, description, wasAttributedTo,
                 startedAtTime, endedAtTime, used_entities, generated_entities)

    g2 = a.get_graph()

    #compare
    iso1 = compare.to_isomorphic(g)
    iso2 = compare.to_isomorphic(g2)
    in_both, in_first, in_second = compare.graph_diff(iso1, iso2)

    print str(len(in_both)) + ', ' + str(len(in_first)) + ', ' + str(len(
        in_second))

    assert len(in_first) == 0
    assert len(in_second) == 0


def test_activity_external():
    #TODO: implement same as above but with dummy used & generated Entities
    pass