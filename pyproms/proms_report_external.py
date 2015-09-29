from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.proms_report import PromsReport
from pyproms.prov_activity import ProvActivity
from pyproms.proms_activity import PromsActivity
from proms_error import PromsDataModelError


class PromsExternalReport(PromsReport):
    """
    Creates a PROMS-O Basic Report instance
    
    This has no new features on top of Report but it's worth maintaining the separate classes
    """
    def __init__(self,
                 label,
                 reportingSystem,
                 nativeId,
                 reportActivity,
                 comment=None):
        
        PromsReport.__init__(self,
                                  label,
                                  reportingSystem,
                                  nativeId,
                                  comment)

        self.__set_reportActivity(reportActivity)

    def __set_reportActivity(self, reportActivity):
        if (type(reportActivity) is ProvActivity or
            type(reportActivity) is PromsActivity):
            self.reportActivity = reportActivity
        else:
            raise TypeError('reportActivity must be an Agent, not a %s' % type(reportActivity))

    def make_graph(self):
        """
        Specialises PromsReport.make_graph()

        :return: an rdflib Graph object
        """
        PromsReport.make_graph(self)

        PROMS = Namespace('http://promsns.org/def/proms#')

        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.BasicReport))

        self.g = self.g + self.reportActivity.get_graph()

        self.g.add((URIRef(self.uri),
                    PROMS.startingActivity,
                    URIRef(self.reportActivity.uri)))