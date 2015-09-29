from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF
from pyproms.owlclass import OwlClass
from pyproms.proms_reportingsystem import PromsReportingSystem
import uuid


class PromsReport(OwlClass):
    """
    Creates a PROV-O Report instance
    """
    def __init__(self,
                 label,
                 reportingSystem,
                 nativeId,
                 comment=None):

        OwlClass.__init__(self, label, comment)

        self.uri = 'http://placeholder.org#' + str(uuid.uuid4())
        self.__set_reportingSystem(reportingSystem)
        if type(nativeId) is str:
            self.nativeId = nativeId
        else:
            raise TypeError('nativeId must be a String (str), not a %s' % type(nativeId))

    def __set_reportingSystem(self, reportingSystem):
        if type(reportingSystem) is PromsReportingSystem:
            self.reportingSystem = reportingSystem
        else:
            raise TypeError('reportingSystem must be a PromsReportingSystem, not a %s' % type(reportingSystem))

    def make_graph(self):
        """
        Specialises RdfClass.make_graph()

        :return: an rdflib Graph object
        """
        OwlClass.make_graph(self)

        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.Report))

        self.g = self.g + self.reportingSystem.get_graph()
        self.g.add((URIRef(self.uri),
                    PROMS.reportingSystem,
                    URIRef(self.reportingSystem.uri)))

        self.g.add((URIRef(self.uri),
                    PROMS.nativeId,
                    Literal(self.nativeId, datatype=XSD.string)))