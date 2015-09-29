from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.owlclass import OwlClass
from pyproms.prov_activity import ProvActivity
import re


# TODO: fix the recursion issue wrt wasAssociatedWith values
class PromsActivity(ProvActivity):
    """
    Creates a PROMS-O Activity instance
    """
    def __init__(self,
                 label,
                 startedAtTime,
                 endedAtTime,
                 uri=None,
                 wasAssociatedWith=None,
                 comment=None,
                 used_entities=None,
                 generated_entities=None,
                 wasInformedBy=None,
                 namedActivityUri=None):

        PromsActivity.__init__(self,
                               label,
                               uri=uri,
                               wasAssociatedWith=wasAssociatedWith,
                               startedAtTime=startedAtTime,
                               endedAtTime=endedAtTime,
                               comment=comment,
                               used_entities=used_entities,
                               generated_entities=generated_entities,
                               wasInformedBy=wasInformedBy)

        # set PROMS Activity-only properties
        self.namedActivityUri = self.set_namedActivityUri(namedActivityUri)

    def set_namedActivityUri(self, namedActivityUri):
        """
        Sets a wasAssociatedWith property for this Activity to another Activity
        indicated via a URI

        :param namedActivityUri: URIRef or string
        :return: -
        """
        if type(namedActivityUri) is URIRef:
            self.namedActivityUri = str(namedActivityUri)
        elif type(namedActivityUri) is str:
            # it's a string so we need to validate it via REGEX
            # Django's URL validator
            regex = re.compile(
                    r'^(?:http|ftp)s?://' # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                    r'localhost|' #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?' # optional port
                    r'(?:/?|[/?]\S+)$',
                    re.IGNORECASE)
            # our modified validator
            # TODO: implement different from Django's
            if regex.match(namedActivityUri):
                self.namedActivityUri = namedActivityUri
        else:
            raise TypeError('wasAssociatedWith must be an Activity, not a %s' % type(namedActivityUri))

    def make_graph(self):
        """
        Specialises ProvActivity.make_graph()

        :return: an rdflib Graph object
        """
        ProvActivity.make_graph(self)

        # add in a type of PROMS Activity
        PROMS = Namespace('http://promsns.org/def/proms#')
        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.Entity))

        if self.namedActivityUri:
            self.g.add((URIRef(self.uri),
                        PROMS.namedActivityUri,
                        URIRef(self.wasInformedBy)))