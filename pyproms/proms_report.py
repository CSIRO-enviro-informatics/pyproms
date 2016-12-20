from datetime import datetime
from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import RDF, OWL
from pyproms.owlclass import OwlClass
from pyproms.proms_reportingsystem import PromsReportingSystem
from pyproms.prov_activity import ProvActivity
import uuid


class PromsReport(OwlClass):
    """
    Creates a PROV-O Report instance
    """
    def __init__(self,
                 label,
                 wasReportedBy,
                 nativeId,
                 reportActivity,
                 generatedAtTime,
                 comment=None):

        OwlClass.__init__(self, label, comment)

        self.uri = 'http://placeholder.org#' + str(uuid.uuid4())
        self.__set_wasReportedBy(wasReportedBy)
        self.__set_nativeId(nativeId)
        self.__set_reportActivity(reportActivity)
        self.__set_generatedAtTime(generatedAtTime)

    def __set_wasReportedBy(self, wasReportedBy):
        if type(wasReportedBy) is PromsReportingSystem:
            self.wasReportedBy = wasReportedBy
        else:
            raise TypeError('wasReportedBy must be a ReportingSystem, not a %s' % type(wasReportedBy))

    def __set_nativeId(self, nativeId):
        if type(nativeId) is str:
            self.nativeId = nativeId
        else:
            raise TypeError('nativeId must be a string (str), not a %s' % type(nativeId))

    def __set_reportActivity(self, reportActivity):
        if type(reportActivity) is ProvActivity:
            self.reportActivity = reportActivity
        else:
            raise TypeError('reportActivity must be an Agent, not a %s' % type(reportActivity))

    def __set_generatedAtTime(self, generatedAtTime):
        if type(generatedAtTime) is datetime:
            self.generatedAtTime = generatedAtTime
        else:
            raise TypeError('endedAtTime must be a datetime.datetime, not a %s' % type(generatedAtTime))

    def make_graph(self):
        """
        Specialises RdfClass.make_graph()

        :return: an rdflib Graph object
        """
        OwlClass.make_graph(self)

        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        PROV = Namespace('http://www.w3.org/ns/prov#')
        self.g.bind('prov', PROV)
        PROMS = Namespace('http://promsns.org/def/proms#')
        self.g.bind('proms', PROMS)

        self.g.remove((
            URIRef(self.uri),
            RDF.type,
            OWL.Class))
        self.g.add((
            URIRef(self.uri),
            RDF.type,
            PROMS.Report))

        self.g = self.g + self.wasReportedBy.get_graph()

        self.g.add((URIRef(self.uri),
                    PROMS.wasReportedBy,
                    URIRef(self.wasReportedBy.uri)))

        self.g.add((URIRef(self.uri),
                    PROMS.nativeId,
                    Literal(self.nativeId, datatype=XSD.string)))

        self.g = self.g + self.reportActivity.get_graph()

        self.g.add((URIRef(self.uri),
                    PROMS.startingActivity,
                    URIRef(self.reportActivity.uri)))

        self.g.add((URIRef(self.uri),
                    PROMS.endingActivity,
                    URIRef(self.reportActivity.uri)))

        self.g.add((URIRef(self.uri),
                    PROV.generatedAtTime,
                    Literal(self.generatedAtTime.isoformat(), datatype=XSD.dateTime)))
