import datetime
from rdflib import URIRef, Namespace, Graph, Literal, BNode, compare, serializer
from rdflib.namespace import RDF
from pyproms import entity


def test_entity_defined_elsewhere():
    entity_uri = 'http://promsns.org/demo/abc-123'
    #create an Entity by hand for comparison and make graph
    g = Graph()
    PROV = Namespace('http://www.w3.org/ns/prov#')
    g.add((URIRef(entity_uri), RDF.type, PROV.Entity))

    #instantiate Entity & get_graph
    g2 = Graph()
    e = entity.Entity(entity_uri, None, None, None, None,
                      None, None, None, None)

    g2 = e.get_graph()

    #compare
    iso1 = compare.to_isomorphic(g)
    iso2 = compare.to_isomorphic(g2)
    in_both, in_first, in_second = compare.graph_diff(iso1, iso2)

    #print str(len(in_both)) + ', ' + str(len(in_first)) + ', ' + str(len(
    # in_second))

    assert len(in_first) == 0
    assert len(in_second) == 0


def test_entity_defined_here():
    #create an Entity by hand for comparison and make graph
    entity_uri = URIRef(BNode())
    title = "Test Entity"
    description = "This is a tests Entity"
    created = datetime.datetime.strptime("2014-06-23T10:15:16",
                                         "%Y-%m-%dT%H:%M:%S")
    creator = 'http://data.bioregionalassessments.gov.au/person/car587'
    confidentialityStatus = entity.ConfidentialityStatus.PublicDomain
    metadataUri = 'http://example.com/a_uri'
    dataUri = 'http://example.com/another_uri'

    g = Graph()
    PROV = Namespace('http://www.w3.org/ns/prov#')
    XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
    PROMS = Namespace('http://promsns.org/def/proms#')
    DC = Namespace('http://purl.org/dc/elements/1.1/')

    g.add((entity_uri, RDF.type, PROV.Entity))
    g.add((entity_uri, DC.title, Literal(title, datatype=XSD.string)))
    g.add((entity_uri, DC.description, Literal(description,
                                               datatype=XSD.string)))
    g.add((entity_uri, DC.created,
           Literal(created.strftime("%Y-%m-%dT%H:%M:%S"),
                   datatype=XSD.dateTime)))
    g.add((entity_uri, DC.creator, Literal(creator, datatype=XSD.anyUri)))
    g.add((entity_uri,
           DC.license, Literal(license, datatype=XSD.anyUri)))
    g.add((entity_uri, PROMS.confidentialityStatus,
           Literal(confidentialityStatus, datatype=XSD.anyUri)))
    g.add((entity_uri, PROMS.metadataUri, Literal(
        metadataUri, datatype=XSD.anyUri)))
    g.add((entity_uri, PROMS.dataUri, Literal(
        dataUri, datatype=XSD.anyUri)))

    #instantiate Entity & get_graph
    e = entity.Entity(entity_uri, title, description, created, creator,
                      license, confidentialityStatus, metadataUri, dataUri)

    g2 = e.get_graph()

    #compare
    iso1 = compare.to_isomorphic(g)
    iso2 = compare.to_isomorphic(g2)
    in_both, in_first, in_second = compare.graph_diff(iso1, iso2)

    print(str(len(in_both)) + ', ' + str(len(in_first)) + ', ' + str(len(
        in_second)))

    print(in_first.serialize(format='n3'))
    print(in_second.serialize(format='n3'))
    print(in_both.serialize(format='n3'))

    assert len(in_first) == 0
    assert len(in_second) == 0