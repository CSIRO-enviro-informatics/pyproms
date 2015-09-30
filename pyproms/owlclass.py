from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS, OWL
import uuid


class OwlClass(object):
    """
    This class creates generic RDF classes that require only an rdfs:label
    property to be specified. It is mostly used by inheritance to produce
    specialised RDF classes, such as Report or Entity.
    """
    def __init__(self,
                 label,
                 uri=None,
                 comment=None):
        self.g = None
        self.label = label
        if uri:
            self.uri = uri
        else:
            self.uri = 'http://placeholder.org#' + str(uuid.uuid4())
        self.comment = comment

    def set_uri(self, uri):
        self.uri = uri

    def set_comment(self, comment):
        self.comment = comment

    def make_graph(self):
        """
        Constructs an RDF graph for this class using its instance variables

        :return: an rdflib Graph object
        """
        self.g = Graph()

        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    OWL.Class))

        self.g.add((URIRef(self.uri),
                    RDFS.label,
                    Literal(self.label, datatype=XSD.string)))

        if self.comment:
            self.g.add((URIRef(self.uri),
                        RDFS.comment,
                        Literal(self.comment, datatype=XSD.string)))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g

    def serialize_graph(self, format='turtle'):
        return self.get_graph().serialize(format=format)