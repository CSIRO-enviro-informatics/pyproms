from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS
from pyproms.rdfclass import RdfClass
from pyproms.activity import Activity
from pyproms.reportingsystem import ReportingSystem
import uuid


class Report(RdfClass):
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
        self.reportType = reportType
        self.reportingSystem = self.__set_reportingSystem(reportingSystem)
        self.nativeId = nativeId
        self.startingActivity = self.__set_startingActivity(startingActivity)
        self.endingActivity = self.__set_endingActivity(endingActivity)

    def __set_reportingSystem(self, reportingSystem):
        if type(reportingSystem) is ReportingSystem:
            self.wasAttributedTo = reportingSystem
        else:
            raise TypeError('reportingSystem must be an Agent, not a %s' % type(reportingSystem))

    def __set_startingActivity(self, startingActivity):
        if type(startingActivity) is Activity:
            self.wasAttributedTo = startingActivity
        else:
            raise TypeError('startingActivity must be an Agent, not a %s' % type(startingActivity))

    def __set_endingActivity(self, endingActivity):
        if type(endingActivity) is Activity:
            self.wasAttributedTo = endingActivity
        else:
            raise TypeError('endingActivity must be an Agent, not a %s' % type(endingActivity))

    def make_graph(self):
        RdfClass.make_graph(self)

        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROV.Entity))

        self.g.add((URIRef(self.uri),
                    RDF.type, 
                    PROMS.Report))
        
        self.g.add((URIRef(self.uri), 
                    PROMS.reportType, 
                    URIRef(self.reportType)))

        self.g.add((URIRef(self.uri),
                    PROMS.reportingSystem,
                    URIRef(self.reportingSystem)))

    def get_graph(self):
        """
        Generates the RDF graph of this Activity

        :return: This Activity's RDF graph according to PROMS-O
        """

        if not self.g:
            self.make_graph()

        return self.g


class ReportType:
    """
    This class specifies acceptable URI values for the proms:reportType
    property of PROMS-O Reports.
    """
    Basic = 'http://promsns.org/def/proms#Basic'
    External = 'http://promsns.org/def/proms#External'
    Internal = 'http://promsns.org/def/proms#Internal'
