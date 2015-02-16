from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.prov_entity import ProvEntity


# TODO: allow Entity - Entity relationships
class PromsEntity(ProvEntity):
    def __init__(self,
                 label,
                 uri=None,
                 comment=None,
                 wasAttributedTo=None,
                 creator=None,
                 created=None,
                 licence=None,
                 confidentialityStatus=None,
                 metadataUri=None,
                 downloadURL=None):

        ProvEntity.__init__(self,
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

        # if there PROMS Entities had properties that PROV Entity didn't have, we would do something with them here

    # overloaded
    def make_graph(self):
        ProvEntity.make_graph(self)

        # add in a type of PROMS Entity --> this is the only PROV/PROMS Entity difference for now
        PROMS = Namespace('http://promsns.org/def/proms#')
        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.Entity))