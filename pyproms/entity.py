from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF
import datetime
import uuid


# TODO: allow Entity - Entity relationships
class Entity:
    def __init__(self,
                 prov_or_proms,
                 title,
                 uri=None,
                 description=None,
                 creator=None,
                 created=None,
                 licence=None,
                 confidentialityStatus=None,
                 metadataUri=None,
                 downloadURL=None):
        self.prov_or_proms = prov_or_proms
        self.g = None
        # set placeholder URI, to be replaces at Report generation time
        if uri:
            self.uri = uri
        else:
            self.uri = 'http://placeholder.org#' + str(uuid.uuid4())

        # title is compulsory
        self.title = title
        self.description = description
        self.creator = creator
        # default created time is now
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now()
        self.licence = licence
        self.confidentialityStatus = confidentialityStatus
        self.metadataUri = metadataUri
        self.downloadURL = downloadURL

    def set_uri(self, uri):
        self.uri = uri

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_creator(self, creator):
        self.creator = creator

    def set_created(self, created):
        self.created = created

    def set_licence(self, licence):
        self.licence = licence

    def set_confidentialityStatus(self, confidentialityStatus):
        self.confidentialityStatus = confidentialityStatus

    def set_metadataUri(self, metadataUri):
        self.metadataUri = metadataUri

    def set_downloadURL(self, downloadURL):
        self.downloadURL = downloadURL

    def make_graph(self):
        self.g = Graph()

        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')
        DC = Namespace('http://purl.org/dc/elements/1.1/')
        DCAT = Namespace('http://www.w3.org/ns/dcat#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Entity))

        # TODO: add Entity to PROMS-O
        if self.prov_or_proms == 'PROMS':
            self.g.add((URIRef(self.uri),
                        RDF.type,
                        PROMS.Entity))

        self.g.add((URIRef(self.uri),
                    DC.title,
                    Literal(self.title, datatype=XSD.string)))
        
        if self.description:
            self.g.add((URIRef(self.uri),
                        DC.title,
                        Literal(self.title, datatype=XSD.string)))        

        if self.creator:
            self.g.add((URIRef(self.uri),
                        DC.creator,
                        URIRef(self.creator)))
        
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

        # TODO review PROMS-O property confidentialityStatus
        if self.confidentialityStatus:
            self.g.add((URIRef(self.uri),
                        PROMS.confidentialityStatus,
                        Literal(self.metadataUri, datatype=XSD.anyUri)))

        if self.metadataUri:
            self.g.add((URIRef(self.uri),
                        PROMS.metadataUri,
                        Literal(self.metadataUri, datatype=XSD.anyUri)))

        if self.downloadURL:
            self.g.add((URIRef(self.uri),
                        DCAT.downloadURL,
                        Literal(self.downloadURL, datatype=XSD.anyUri)))
        #endregion        

    def get_graph(self):
        """
        Generates the RDF graph of this Entity

        :return: This Entity's RDF graph according to PROMS-O
        """

        if not self.g:
            self.make_graph()

        return self.g

    def serialize_graph(self, format='turtle'):
        return self.get_graph().serialize(format=format)


class ConfidentialityStatus:
    """
    This class specifies acceptable URI values for
    the proms:confidentialityStatus property of PROMS-O Entities.
    """
    PublicDomain = 'http://promsns.org/def/proms/confidentiality/publicdomain'
    Private = 'http://promsns.org/def/proms/confidentiality/private'
    AccessAvailableOnRequest = 'http://promsns.org/def/proms/confidentiality/accessavailableonrequest'
    OwnerDepartmentOnly = 'http://promsns.org/def/proms/confidentiality/ownerdepartmentonly'
    IndigenousSensitive = 'http://promsns.org/def/proms/confidentiality/indigenoussensitive'