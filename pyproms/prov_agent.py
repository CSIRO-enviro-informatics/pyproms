from rdflib import URIRef, Namespace
from rdflib.namespace import RDF, OWL
from pyproms.owlclass import OwlClass


# TODO: split Agent into People and Software Agents for more in-depth handling later
class ProvAgent(OwlClass):
    """
    Creates a PROV-O Agent instance
    """
    def __init__(
            self,
            label,
            uri=None,
            comment=None,
            actedOnBehalfOf=None):

        OwlClass.__init__(self, label, uri, comment)

        if actedOnBehalfOf:
            self.set_actedOnBehalfOf(actedOnBehalfOf)
        else:
            self.actedOnBehalfOf = None

    def set_actedOnBehalfOf(self, actedOnBehalfOf):
        if type(actedOnBehalfOf) is ProvAgent:
            self.actedOnBehalfOf = actedOnBehalfOf
        else:
            raise TypeError('wasAttributedTo must be an Agent, not a %s' % type(actedOnBehalfOf))

    def make_graph(self):
        """
        Specialises RdfClass.make_graph()

        :return: an rdflib Graph object
        """
        OwlClass.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        self.g.bind('prov', PROV)

        self.g.remove((
            URIRef(self.uri),
            RDF.type,
            OWL.Class))
        self.g.add((
            URIRef(self.uri),
            RDF.type,
            PROV.Agent))

        if self.actedOnBehalfOf:
            self.g = self.g + self.actedOnBehalfOf.get_graph()
            self.g.add((URIRef(self.uri),
                        PROV.actedOnBehalfOf,
                        URIRef(self.actedOnBehalfOf.uri)))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g
