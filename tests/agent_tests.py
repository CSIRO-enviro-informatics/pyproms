from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF, RDFS, XSD
from pyproms import ProvAgent


def test_agent():
    # create an Agent graph by hand
    PROV = Namespace('http://www.w3.org/ns/prov#')
    g = Graph()

    uri_string = 'http://example.org/agent/1'
    agent_uri = URIRef(uri_string)
    label_string = 'Test Agent'
    agent_label = Literal(label_string, datatype=XSD.string)
    g.add((agent_uri, RDF.type, PROV.Agent))
    g.add((agent_uri, RDFS.label, agent_label))

    # create an Agent via toolkit, get its graph
    a = ProvAgent(label_string, uri_string)
    g2 = a.get_graph()

    assert g.isomorphic(g2)


if __name__ == '__main__':
    test_agent()
