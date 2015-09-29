from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import RDF
import datetime
from pyproms.owlclass import OwlClass
from pyproms.prov_agent import ProvAgent


# TODO: allow Entity - Entity relationships
class ProvEntity(OwlClass):
    """
    Creates a PROV-O Entity instance
    """
    def __init__(self,
                 label,
                 uri=None,
                 comment=None,
                 wasAttributedTo=None,
                 creator=None,
                 created=None,
                 licence=None,
                 metadataUri=None,
                 downloadURL=None,
                 value=None):

        OwlClass.__init__(self, label, uri, comment)

        if wasAttributedTo:
            self.set_wasAttributedTo(wasAttributedTo)
        else:
            self.wasAttributedTo = None
        if creator:
            self.set_creator(creator)
        else:
            self.creator = None
        # default created time is now
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now()
        self.licence = licence
        self.metadataUri = metadataUri
        self.downloadURL = downloadURL
        if value:
            self.set_value(value)
        else:
            self.value = None

    def set_wasAttributedTo(self, wasAttributedTo):
        if type(wasAttributedTo) is ProvAgent:
            self.wasAttributedTo = wasAttributedTo
        else:
            raise TypeError('wasAttributedTo must be an Agent, not a %s' % type(wasAttributedTo))

    def set_creator(self, creator):
        if type(creator) is ProvAgent:
            self.creator = creator
        else:
            raise TypeError('creator must be an Agent, not a %s' % type(creator))

    def set_created(self, created):
        if type(created) is datetime.datetime:
            self.created = created
        else:
            raise TypeError('startedAtTime must be a datetime.datetime, not a %s' % type(created))

    def set_licence(self, licence):
        self.licence = licence

    def set_metadataUri(self, metadataUri):
        self.metadataUri = metadataUri

    def set_downloadURL(self, downloadURL):
        self.downloadURL = downloadURL

    def set_value(self, value):
        if (type(value) is str or
            type(value) is float or
            type(value) is int or
            type(value) is datetime.datetime):
            self.value = value
        else:
            raise TypeError('Entity \'value\' must be a string, int, float or datetime, not a %s' % type(value))

    def make_graph(self):
        """
        Specialises RdfClass.make_graph()

        :return: an rdflib Graph object
        """
        OwlClass.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')
        DC = Namespace('http://purl.org/dc/elements/1.1/')
        DCAT = Namespace('http://www.w3.org/ns/dcat#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Entity))

        if self.wasAttributedTo:
            self.g = self.g + self.wasAttributedTo.get_graph()
            self.g.add((URIRef(self.uri),
                        PROV.wasAttributedTo,
                        URIRef(self.wasAttributedTo.uri)))

        if self.creator:
            self.g = self.g + self.creator.get_graph()
            self.g.add((URIRef(self.uri),
                        PROV.creator,
                        URIRef(self.creator.uri)))
        
        if self.created:
            self.g.add((URIRef(self.uri),
                        DC.created,
                        Literal(self.created.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))
        # TODO: review PROMS-O propertycreatedAtTimeDiffStep
        '''
        else:
            if isinstance(self.created, int):
               self.g.add((URIRef(self.uri),
                           PROMS.createdAtTimeDiffStep,
                           Literal(self.created, datatype=XSD.integer)))
        '''

        if self.licence:
            self.g.add((URIRef(self.uri),
                        DC.licence,
                        Literal(self.metadataUri, datatype=XSD.anyUri)))

        if self.metadataUri:
            self.g.add((URIRef(self.uri),
                        PROMS.metadataUri,
                        Literal(self.metadataUri, datatype=XSD.anyUri)))

        if self.downloadURL:
            self.g.add((URIRef(self.uri),
                        DCAT.downloadURL,
                        Literal(self.downloadURL, datatype=XSD.anyUri)))

        if self.value:
            if (type(self.value) is datetime.datetime):
                self.g.add((URIRef(self.uri),
                            PROV.value,
                            Literal(self.value, datatype=XSD.dateTime)))
            elif (type(self.value) is int):
                self.g.add((URIRef(self.uri),
                            PROV.value,
                            Literal(self.value, datatype=XSD.integer)))
            elif (type(self.value) is float):
                self.g.add((URIRef(self.uri),
                            PROV.value,
                            Literal(self.value, datatype=XSD.float)))
            else:  # string
                self.g.add((URIRef(self.uri),
                            PROV.value,
                            Literal(self.value, datatype=XSD.string)))

    def get_graph(self):
        """
        Generates the RDF graph of this class

        :return: This class's RDF graph
        """
        if not self.g:
            self.make_graph()

        return self.g