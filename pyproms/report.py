from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import RDF


class Report:
    def __init__(self,
                 report_uri=None,
                 reportType=None,
                 title=None,
                 starting_activity=None,
                 startedAtTime=None,
                 ending_activity=None,
                 endedAtTime=None,
                 reportingSystemJobUri=None,
                 description=None):
        """
        Creates objects of type PROMS-O Report

        :param reportType: proms:reportType
        :param title: dc:title
        :param description: dc:description
        :param starting_activity: A proms:Entity
        :param startedAtTime: prov:startedAtTime. Must not be a proms:startedAtTimeDiffStep
        :param ending_activity: A proms:Entity
        :param endedAtTime: prov:endedAtTime. Must not be a proms:endedAtTimeDiffStep
        :return: nothing (a Report object is created)
        """

        #region Set instance variables
        if report_uri:
            self.report_uri = report_uri
        else:
            self.report_uri = URIRef('http://promsns.org/report-placeholder-uri')
        self.reportType = reportType
        self.title = title
        self.starting_activity = starting_activity
        self.startedAtTime = startedAtTime
        self.ending_activity = ending_activity
        self.endedAtTime = endedAtTime
        if reportingSystemJobUri:
            self.reportingSystemJobUri = reportingSystemJobUri
        else:
            self.description = None
        if description:
            self.description = description
        else:
            self.description = None
        #endregion

        #region Add instance variables to graph
        self.g = Graph()

        PROMS = Namespace('http://promsns.org/def/proms#')
        PROV = Namespace('http://www.w3.org/ns/prov#')
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
        DC = Namespace('http://purl.org/dc/elements/1.1/')

        self.g = Graph()
        self.g.add((URIRef(self.report_uri), RDF.type, PROMS.Report))
        self.g.add((URIRef(self.report_uri), PROMS.reportType, URIRef(self.reportType)))
        self.g.add((URIRef(self.report_uri), DC.title, Literal(self.title, datatype=XSD.string)))

        #add the Activity to the graph
        self.g = self.g + self.starting_activity.get_graph()
        #link the Activity to the Report
        self.g.add((URIRef(self.report_uri),
                    PROMS.startingActivity,
                    URIRef(self.starting_activity.get_id())))

        self.g.add((URIRef(self.report_uri),
                    PROV.startedAtTime,
                    Literal(self.startedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))

        #add the Activity to the graph
        self.g = self.g + self.ending_activity.get_graph()
        #link the Activity to the Report
        self.g.add((URIRef(self.report_uri),
                    PROMS.endingActivity,
                    URIRef(self.ending_activity.get_id())))

        self.g.add((URIRef(self.report_uri),
                    PROV.endedAtTime,
                    Literal(self.endedAtTime.strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime)))

        if self.description:
            self.g.add((URIRef(self.report_uri),
                        PROMS.reportingSystemJobUri,
                        URIRef(self.reportingSystemJobUri)))

        if self.description:
            self.g.add((URIRef(self.report_uri),
                        DC.description,
                        Literal(self.description, datatype=XSD.string)))
        #endregion

        return

    def get_id(self):
        """
        Get the node URI of this Report. Always a URI.

        :return: A URI
        """
        return URIRef(self.report_uri)

    def get_graph(self):
        """
        Generates the RDF graph of this Report

        :return: This Report's RDF graph according to PROMS-O
        """
        return self.g


class ReportType:
    """
    This class specifies acceptable URI values for the proms:reportType
    property of PROMS-O Reports.
    """
    Basic = 'http://promsns.org/def/proms#Basic'
    External = 'http://promsns.org/def/proms#External'
    Internal = 'http://promsns.org/def/proms#Internal'
