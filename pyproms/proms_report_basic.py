from rdflib import URIRef, Namespace
from rdflib.namespace import RDF
from pyproms.proms_report import PromsReport


class PromsBasicReport(PromsReport):
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
                             reportActivity,
                             comment)

    def make_graph(self):
        """
        Specialises PromsReport.make_graph()

        :return: an rdflib Graph object
        """
        PromsReport.make_graph(self)

        PROMS = Namespace('http://promsns.org/def/proms#')

        # The only thing we need to do here is to redefine the Report class as BasicReport.
        # There are no additional properties
        self.g.add((URIRef(self.uri),
                    RDF.type,
                    PROMS.BasicReport))