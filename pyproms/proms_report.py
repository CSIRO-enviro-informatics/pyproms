from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF
from pyproms.rdfclass import RdfClass
from pyproms.prov_activity import ProvActivity
from pyproms.proms_reportingsystem import PromsReportingSystem
from pyproms.proms_activity import PromsActivity
import uuid


class PromsReport(RdfClass):
    """
    Creates a PROV-O Report instance
    """
    def __init__(self,
                 label,
                 reportType,
                 reportingSystem,
                 nativeId,
                 startingActivity,
                 endingActivity,
                 comment=None):

        RdfClass.__init__(self, label, comment)

        self.uri = 'http://placeholder.org#' + str(uuid.uuid4())
        if type(reportType) is str:
            self.reportType = reportType
        else:
            raise TypeError('reportType must be a String (str), not a %s' % type(reportType))
        self.__set_reportingSystem(reportingSystem)
        if type(nativeId) is str:
            self.nativeId = nativeId
        else:
            raise TypeError('reportType must be a String (str), not a %s' % type(nativeId))
        self.__set_startingActivity(startingActivity)
        self.__set_endingActivity(endingActivity)

    def __set_reportingSystem(self, reportingSystem):
        if type(reportingSystem) is PromsReportingSystem:
            self.reportingSystem = reportingSystem
        else:
            raise TypeError('reportingSystem must be a PromsReportingSystem, not a %s' % type(reportingSystem))

    def __set_startingActivity(self, startingActivity):
        if (type(startingActivity) is ProvActivity or
            type(startingActivity) is PromsActivity):
            self.startingActivity = startingActivity
        else:
            raise TypeError('startingActivity must be an Agent, not a %s' % type(startingActivity))

    def __set_endingActivity(self, endingActivity):
        if (type(endingActivity) is ProvActivity or
            type(endingActivity) is PromsActivity):
            self.endingActivity = endingActivity
        else:
            raise TypeError('endingActivity must be an Agent, not a %s' % type(endingActivity))

    def make_graph(self):
        """
        Specialises RdfClass.make_graph()

        :return: an rdflib Graph object
        """
        RdfClass.make_graph(self)

        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type, 
                    PROMS.Report))

        self.g.add((URIRef(self.uri), 
                    PROMS.reportType, 
                    URIRef(self.reportType)))

        self.g = self.g + self.reportingSystem.get_graph()
        self.g.add((URIRef(self.uri),
                    PROMS.reportingSystem,
                    URIRef(self.reportingSystem.uri)))

        self.g.add((URIRef(self.uri),
                        PROMS.nativeId,
                        Literal(self.nativeId, datatype=XSD.string)))

        self.g = self.g + self.startingActivity.get_graph()
        self.g.add((URIRef(self.uri),
                    PROMS.startingActivity,
                    URIRef(self.startingActivity.uri)))

        self.g = self.g + self.endingActivity.get_graph()
        self.g.add((URIRef(self.uri),
                    PROMS.endingActivity,
                    URIRef(self.endingActivity.uri)))


class ReportType(object):
    """
    This class specifies acceptable URI values for the proms:reportType
    property of PROMS-O Reports.
    """
    Basic = 'http://promsns.org/def/proms#Basic'
    External = 'http://promsns.org/def/proms#External'
    Internal = 'http://promsns.org/def/proms#Internal'
