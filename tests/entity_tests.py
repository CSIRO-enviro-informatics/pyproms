from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF, RDFS, XSD
from pyproms.prov_entity import ProvEntity


def test_entity_defined_elsewhere_minimal():
    # create an Entity graph by hand
    g = Graph()
    PROV = Namespace('http://www.w3.org/ns/prov#')

    entity_label_string = 'Test Entity'
    entity_label = Literal(entity_label_string, datatype=XSD.string)
    entity_uri_string = 'http://promsns.org/demo/abc-123'
    entity_uri = URIRef(entity_uri_string)

    g.add((entity_uri, RDF.type, PROV.Entity))
    g.add((entity_uri, RDFS.label, entity_label))

    # create an Entity via toolkit, get its graph
    e = ProvEntity(entity_label_string, entity_uri_string)
    g2 = e.get_graph()

    assert g.isomorphic(g2)


def test_entity_defined_here_minmal():
    # create an Entity graph by hand
    PROV = Namespace('http://www.w3.org/ns/prov#')
    XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
    g = Graph()

    entity_label_string = 'Test Entity'
    entity_label = Literal(entity_label_string, datatype=XSD.string)
    entity_uri_string = 'http://promsns.org/demo/abc-123'
    entity_uri = URIRef(entity_uri_string)
    value = Literal(42, datatype=XSD.integer)

    g.add((entity_uri, RDF.type, PROV.Entity))
    g.add((entity_uri, RDFS.label, entity_label))
    g.add((entity_uri, PROV.value, value))

    # create an Entity via toolkit, get its graph
    e = ProvEntity(entity_label_string, entity_uri_string, None, None, 42) # TODO: replace fixed URI with a BNode
    g2 = e.get_graph()

    assert g.isomorphic(g2)


if __name__ == '__main__':
    test_entity_defined_elsewhere_minimal()
    test_entity_defined_here_minmal()

