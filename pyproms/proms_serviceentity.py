from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF
from pyproms.proms_entity import PromsEntity
import datetime


# TODO: allow Entity - Entity relationships
class PromsServiceEntity(PromsEntity):
    """
    Creates a PROMS-O ServiceEntity instance
    """
    def __init__(self,
                 label,
                 serviceBaseUri,
                 query,
                 queriedAtTime,
                 cachedCopyUri=None,
                 uri=None,
                 comment=None,
                 wasAttributedTo=None,
                 creator=None,
                 created=None,
                 licence=None,
                 confidentialityStatus=None,
                 metadataUri=None,
                 downloadURL=None):

        PromsEntity.__init__(self,
                             label,
                             uri=uri,
                             comment=comment,
                             wasAttributedTo=wasAttributedTo,
                             creator=creator,
                             created=created,
                             licence=licence,
                             confidentialityStatus=confidentialityStatus,
                             metadataUri=metadataUri,
                             downloadURL=downloadURL)

        # the additional properties of a proms:ServiceEntity over a proms:Entity
        self.serviceBaseUri = serviceBaseUri
        self.query = query
        self.queriedAtTime = queriedAtTime
        self.cachedCopyUri = cachedCopyUri

    def set_serviceBaseUri(self, serviceBaseUri):
        self.serviceBaseUri = serviceBaseUri

    def set_query(self, query):
        self.query = query

    def set_queriedAtTime(self, queriedAtTime):
        if type(queriedAtTime) is datetime.datetime:
            self.queriedAtTime = queriedAtTime
        else:
            raise TypeError('startedAtTime must be a datetime.datetime, not a %s' % type(queriedAtTime))

    # TODO: add a type check constraint here and in constructor: URIRef or anyUri?
    def set_cachedCopyUri(self, cachedCopyUri):
        self.cachedCopyUri = cachedCopyUri

    # overloaded
    def make_graph(self):
        """
        Specialises PromsEntity.make_graph()

        :return: an rdflib Graph object
        """
        PromsEntity.make_graph(self)

        # add in a type of PROMS Entity --> this is the only PROV/PROMS Entity difference for now
        PROMS = Namespace('http://promsns.org/def/proms#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.ServiceEntity))

        self.g.add((URIRef(self.uri),
                    PROMS.serviceBaseUri,
                    Literal(self.serviceBaseUri, datatype=XSD.anyUri)))

        self.g.add((URIRef(self.uri),
                    PROMS.query,
                    Literal(self.query, datatype=XSD.string)))

        self.g.add((URIRef(self.uri),
                    PROMS.queriedAtTime,
                    Literal(self.queriedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))