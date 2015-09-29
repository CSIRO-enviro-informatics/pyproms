from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import RDF, FOAF
from pyproms.owlclass import OwlClass


# TODO: split Agent into People and Software Agents for more in-depth handling later
class ProvAgent(OwlClass):
    """
    Creates a PROV-O Agent instance
    """
    def __init__(self,
                 label,
                 uri=None,
                 comment=None,
                 actedOnBehalfOf=None,
                 name=None,
                 givenName=None,
                 familyName=None,
                 mbox=None):

        OwlClass.__init__(self, label, uri, comment)

        if actedOnBehalfOf:
            self.set_actedOnBehalfOf(actedOnBehalfOf)
        else:
            self.actedOnBehalfOf = None
        self.name = name
        self.givenName = givenName
        self.familyName = familyName
        self.mbox = mbox

    def set_actedOnBehalfOf(self, actedOnBehalfOf):
        if type(actedOnBehalfOf) is ProvAgent:
            self.actedOnBehalfOf = actedOnBehalfOf
        else:
            raise TypeError('wasAttributedTo must be an Agent, not a %s' % type(actedOnBehalfOf))

    def set_name(self, name):
        self.name = name

    def set_givenName(self, givenName):
        self.givenName = givenName

    def set_familyName(self, familyName):
        self.familyName = familyName

    def set_mbox(self, mbox):
        self.mbox = mbox

    def make_graph(self):
        """
        Specialises RdfClass.make_graph()

        :return: an rdflib Graph object
        """
        OwlClass.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Agent))

        if self.actedOnBehalfOf:
            self.g = self.g + self.actedOnBehalfOf.get_graph()
            self.g.add((URIRef(self.uri),
                        PROV.actedOnBehalfOf,
                        URIRef(self.actedOnBehalfOf.uri)))

        if self.name:
            self.g.add((URIRef(self.uri),
                        FOAF.name,
                        Literal(self.name, datatype=XSD.string)))

        if self.givenName:
            self.g.add((URIRef(self.uri),
                        FOAF.givenName,
                        Literal(self.givenName, datatype=XSD.string)))

        if self.familyName:
            self.g.add((URIRef(self.uri),
                        FOAF.familyName,
                        Literal(self.familyName, datatype=XSD.string)))

        if self.mbox:
            self.g.add((URIRef(self.uri),
                        FOAF.mbox,
                        Literal(self.mbox, datatype=XSD.string)))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g