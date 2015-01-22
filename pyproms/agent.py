from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import RDF, FOAF
from pyproms.rdfclass import RdfClass


class Agent(RdfClass):
    def __init__(self,
                 prov_or_proms,
                 label,
                 uri=None,
                 comment=None,
                 actedOnBehalfOf=None,
                 name=None,
                 givenName=None,
                 familyName=None,
                 mbox=None):

        RdfClass.__init__(self, label, uri, comment)

        self.prov_or_proms = prov_or_proms
        if actedOnBehalfOf:
            self.set_actedOnBehalfOf(actedOnBehalfOf)
        else:
            self.actedOnBehalfOf = None
        self.name = name
        self.givenName = givenName
        self.familyName = familyName
        self.mbox = mbox

    def set_actedOnBehalfOf(self, actedOnBehalfOf):
        if type(actedOnBehalfOf) is Agent:
            self.actedOnBehalfOf = actedOnBehalfOf
        else:
            raise TypeError('actedOnBehalfOf must be an Agent, not a %s' % type(actedOnBehalfOf))

    def set_name(self, name):
        self.name = name

    def set_givenName(self, givenName):
        self.givenName = givenName

    def set_familyName(self, familyName):
        self.familyName = familyName

    def set_mbox(self, mbox):
        self.mbox = mbox

    def make_graph(self):
        RdfClass.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Activity))

        # TODO: add Activity to PROMS-O
        if self.prov_or_proms == 'PROMS':
            self.g.add((URIRef(self.uri),
                        RDF.type,
                        PROMS.Activity))

        if self.actedOnBehalfOf:
            self.g.add((URIRef(self.uri),
                        PROV.actedOnBehalfOf,
                        URIRef(self.actedOnBehalfOf)))

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