from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.rdfclass import RdfClass


# TODO: convert this to a subclass of type Agent, not directly from RdfClass
class PromsReportingSystem(RdfClass):
    def __init__(self,
                 label,
                 uri=None,
                 comment=None):

        RdfClass.__init__(self, label, uri, comment)

    def make_graph(self):
        RdfClass.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Agent))

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.ReportingSystem))