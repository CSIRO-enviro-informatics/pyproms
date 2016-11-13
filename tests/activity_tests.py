import datetime
from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF, RDFS, XSD
from pyproms import ProvActivity
from pyproms import ProvAgent


def test_activity_basic_minimal():
    # create an Activity graph by hand
    PROV = Namespace('http://www.w3.org/ns/prov#')
    g = Graph()

    activity_uri_string = 'http://promsns.org/demo/abc-123'
    activity_uri = URIRef(activity_uri_string)
    label_string = 'Test Activity'
    label = Literal(label_string, datatype=XSD.string)
    wasAssociatedWith = ProvAgent(
        'Nicholas Car',
        'http://example.com/person/nicholas.car',
        None,
        None)
    startedAtTime = datetime.datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    endedAtTime = datetime.datetime.strptime('2014-01-01T12:13:24', '%Y-%m-%dT%H:%M:%S')

    # add the Agent
    g = g + wasAssociatedWith.get_graph()

    # fill out the Activity
    g.add((activity_uri, RDF.type, PROV.Activity))
    g.add((activity_uri, RDFS.label, label))
    g.add((activity_uri, PROV.wasAssociatedWith, URIRef(wasAssociatedWith.uri)))
    g.add((activity_uri, PROV.startedAtTime, Literal(
        startedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))
    g.add(((activity_uri, PROV.endedAtTime, Literal(
        endedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime))))

    # create an Activity using the toolkit, get its graph
    a = ProvActivity(
        label_string,
        startedAtTime,
        endedAtTime,
        wasAssociatedWith,
        activity_uri_string
    )
    g2 = a.get_graph()


def test_activity_external():
    # TODO: implement same as above but with dummy used & generated Entities
    pass


if __name__ == '__main__':
    test_activity_basic_minimal()
