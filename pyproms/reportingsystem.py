from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS
from pyproms.rdfclass import RdfClass


class ReportingSystem(RdfClass):
    def __init__(self,
                 uri,
                 label,
                 comment=None):

        RdfClass.__init__(self, uri, label, comment)

    def make_graph(self):
        self.g = Graph()

        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.ReportingSystem))

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Agent))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g