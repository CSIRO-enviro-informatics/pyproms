from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.prov_agent import ProvAgent


# TODO: convert this to a subclass of type Agent, not directly from RdfClass
class PromsReportingSystem(ProvAgent):
    """
    Creates a PROMS-O ReportingAystem instance
    """
    def __init__(self,
                 label,
                 uri=None,
                 comment=None,
                 name=None,
                 actedOnBehalfOf=None):

        # these variables are not allowed for a ReportingSystem specialisation of prov:Agent
        givenName = None
        familyName = None
        mbox = None

        ProvAgent.__init__(self,
                           label,
                           uri=uri,
                           comment=comment,
                           actedOnBehalfOf=actedOnBehalfOf,
                           name=name,
                           givenName=givenName,
                           familyName=familyName,
                           mbox=mbox)

    def make_graph(self):
        """
        Specialises ProvAgent.make_graph()

        :return: an rdflib Graph object
        """
        ProvAgent.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Agent))

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.ReportingSystem))