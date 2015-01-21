import datetime
from rdflib import URIRef, Namespace, Graph, Literal, BNode, compare, serializer
from rdflib.namespace import RDF, XSD
from pyproms import report, activity


def test_report_basic():
    report_uri = URIRef('http://promsns.org/placeholder')
    reportType = report.ReportType.Basic
    title = 'Test Report'
    description = 'A tests Report'
    wasAttributedTo = 'http://example.com/person/nicholas.car'
    startedAtTime = datetime.datetime.strptime('2014-01-01T12:13:14',
                                               '%Y-%m-%dT%H:%M:%S')
    endedAtTime = datetime.datetime.strptime('2014-01-01T12:13:24',
                                               '%Y-%m-%dT%H:%M:%S')
    starting_activity = activity.Activity('http://promsns.org/demo/abc-123',
                                          'Start Activity',
                                          'A tests start Activity',
                                          wasAttributedTo,
                                          startedAtTime,
                                          endedAtTime,
                                          None,
                                          None)

    ending_activity = activity.Activity('http://promsns.org/demo/abc-456',
                                          'End Activity',
                                          'A tests end Activity',
                                          wasAttributedTo,
                                          startedAtTime,
                                          endedAtTime,
                                          None,
                                          None)


    #create an Activity by hand for comparison and make graph
    PROMS = Namespace('http://promsns.org/def/proms#')
    PROV = Namespace('http://www.w3.org/ns/prov#')
    DC = Namespace('http://purl.org/dc/elements/1.1/')

    g = Graph()

    g.add((URIRef(report_uri), RDF.type, PROMS.Report))
    g.add((URIRef(report_uri), PROMS.reportType, reportType))
    g.add((URIRef(report_uri), DC.title, Literal(title, datatype=XSD.string)))
    g.add((URIRef(report_uri), DC.description, Literal(description,
                                                       datatype=XSD.string)))
    g.add((URIRef(report_uri), PROMS.startingActivity,
           URIRef(starting_activity.get_node_id())))
    g.add((URIRef(report_uri),
           PROV.startedAtTime,
           Literal(startedAtTime.strftime("%Y-%m-%dT%H:%M:%S"),
                   datatype=XSD.dateTime)))
    g.add((URIRef(report_uri), PROMS.endingActivity,
           URIRef(ending_activity.get_node_id())))
    g.add((URIRef(report_uri),
           PROV.endedAtTime,
           Literal(endedAtTime.strftime("%Y-%m-%dT%H:%M:%S"),
                   datatype=XSD.dateTime)))

    #instantiate Activity & get_graph
    a = report.Report(reportType, title, description,
                      starting_activity.get_node_id(),
                      startedAtTime, ending_activity.get_node_id(), endedAtTime)

    g2 = a.get_graph()

    #compare
    iso1 = compare.to_isomorphic(g)
    iso2 = compare.to_isomorphic(g2)
    in_both, in_first, in_second = compare.graph_diff(iso1, iso2)

    #print str(len(in_both)) + ', ' + str(len(in_first)) + ', ' + str(len(
    #    in_second))

    assert len(in_first) == 0
    assert len(in_second) == 0
