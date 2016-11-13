import logging
from datetime import datetime
from rdflib import URIRef, Namespace, Graph, Literal, compare
from rdflib.namespace import RDF, RDFS, XSD
from pyproms import PromsReportingSystem, ProvActivity, ProvEntity, PromsBasicReport, PromsExternalReport, \
    PromsInternalReport


def test_report_basic_minimal():
    # create a Report graph by hand
    g = Graph()
    PROV = Namespace('http://www.w3.org/ns/prov#')
    PROMS = Namespace('http://promsns.org/def/proms#')

    # the Report's basic properties
    report_uri_string = 'http://promsns.org/placeholder'
    report_uri = URIRef(report_uri_string)
    report_label_string = 'Test Report'
    report_label = Literal(report_label_string, datatype=XSD.string)
    wasReportedBy = PromsReportingSystem(
        'System X',
        'http://example.com/system/system-x')
    generatedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    generatedAtTime = Literal(generatedAtTime_date.isoformat(), datatype=XSD.dateTime)
    nativeId_string = 'ABC123'
    nativeId = Literal(nativeId_string, datatype=XSD.string)

    # the Report's Activity
    activity_uri_string = 'http://promsns.org/demo/abc-123'
    activity_label_string = 'Test Activity'
    startedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    endedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    a = ProvActivity(
        activity_label_string,
        startedAtTime_date,
        endedAtTime_date,
        None,
        activity_uri_string)

    # the triples
    g.add((report_uri, RDF.type, PROMS.BasicReport))
    g.add((report_uri, RDFS.label, report_label))
    g.add((report_uri, PROMS.wasReportedBy, URIRef(wasReportedBy.uri)))
    g.add((report_uri, PROMS.startingActivity, URIRef(a.uri)))
    g.add((report_uri, PROMS.endingActivity, URIRef(a.uri)))
    g.add((report_uri, PROMS.nativeId, nativeId))
    g.add((report_uri, PROV.generatedAtTime, generatedAtTime))

    # add the Agent's graph
    g = g + wasReportedBy.get_graph()

    # add the Activity's graph
    g = g + a.get_graph()

    # create a Report via toolkit, get its graph
    r = PromsBasicReport(report_label_string, wasReportedBy, nativeId_string, a, generatedAtTime_date)

    g2 = r.get_graph()

    # replace the auto-assigned URI of the Report with the same one used for the hand made copy
    g2.update(
        '''
        PREFIX proms: <http://promsns.org/def/proms#>
        DELETE {
            ?s ?p ?o
        }
        INSERT {
            <''' + report_uri_string + '''> ?p ?o
        }
        WHERE {
            ?s a proms:BasicReport .
            ?s ?p ?o .
        }
        '''
    )

    assert g.isomorphic(g2)


def test_report_external_minimal():
    # create a Report graph by hand
    g = Graph()
    PROV = Namespace('http://www.w3.org/ns/prov#')
    PROMS = Namespace('http://promsns.org/def/proms#')

    # the Report's basic properties
    report_uri_string = 'http://promsns.org/placeholder'
    report_uri = URIRef(report_uri_string)
    report_label_string = 'Test Report'
    report_label = Literal(report_label_string, datatype=XSD.string)
    wasReportedBy = PromsReportingSystem(
        'System X',
        'http://example.com/system/system-x')
    generatedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    generatedAtTime = Literal(generatedAtTime_date.isoformat(), datatype=XSD.dateTime)
    nativeId_string = 'ABC123'
    nativeId = Literal(nativeId_string, datatype=XSD.string)

    # two input Entities
    e1_label_string = 'Input Entity 1'
    e1_uri_string = 'http://ecat.ga.gov.au/dataset/12'
    e1 = ProvEntity(e1_label_string, e1_uri_string)

    e2_label_string = 'Input Entity 2'
    e2_uri_string = 'http://ecat.ga.gov.au/dataset/13'
    e2_value = 42
    e2 = ProvEntity(e2_label_string, e2_uri_string, None, None, e2_value)

    # an output Entity
    e_out_label_string = 'Output Entity'
    e_out_uri_string = 'http://ecat.ga.gov.au/dataset/14'
    e_out = ProvEntity(e_out_label_string, e_out_uri_string)

    # the Report's Activity
    activity_uri_string = 'http://promsns.org/demo/abc-123'
    activity_label_string = 'Test Activity'
    startedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    endedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    a = ProvActivity(
        activity_label_string,
        startedAtTime_date,
        endedAtTime_date,
        None,
        activity_uri_string,
        None,
        [e1, e2],
        [e_out]
    )

    # the triples
    g.add((report_uri, RDF.type, PROMS.ExternalReport))
    g.add((report_uri, RDFS.label, report_label))
    g.add((report_uri, PROMS.wasReportedBy, URIRef(wasReportedBy.uri)))
    g.add((report_uri, PROMS.startingActivity, URIRef(a.uri)))
    g.add((report_uri, PROMS.endingActivity, URIRef(a.uri)))
    g.add((report_uri, PROMS.nativeId, nativeId))
    g.add((report_uri, PROV.generatedAtTime, generatedAtTime))

    # add the Agent's graph
    g = g + wasReportedBy.get_graph()

    # add the Activity's graph
    g = g + a.get_graph()

    # create a Report via toolkit, get its graph
    r = PromsExternalReport(
        report_label_string,
        wasReportedBy,
        nativeId_string,
        a,
        generatedAtTime_date)

    g2 = r.get_graph()

    # replace the auto-assigned URI of the Report with the same one used for the hand made copy
    g2.update(
        '''
        PREFIX proms: <http://promsns.org/def/proms#>
        DELETE {
            ?s ?p ?o
        }
        INSERT {
            <''' + report_uri_string + '''> ?p ?o
        }
        WHERE {
            ?s a proms:ExternalReport .
            ?s ?p ?o .
        }
        '''
    )

    assert g.isomorphic(g2)


def test_report_internal_minimal():
    # create a Report graph by hand
    g = Graph()
    PROV = Namespace('http://www.w3.org/ns/prov#')
    PROMS = Namespace('http://promsns.org/def/proms#')

    # the Report's basic properties
    report_uri_string = 'http://promsns.org/placeholder'
    report_uri = URIRef(report_uri_string)
    report_label_string = 'Test Report'
    report_label = Literal(report_label_string, datatype=XSD.string)
    wasReportedBy = PromsReportingSystem(
        'System X',
        'http://example.com/system/system-x')
    generatedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    generatedAtTime = Literal(generatedAtTime_date.isoformat(), datatype=XSD.dateTime)
    nativeId_string = 'ABC123'
    nativeId = Literal(nativeId_string, datatype=XSD.string)

    # two input Entities
    e1_label_string = 'Input Entity 1'
    e1_uri_string = 'http://ecat.ga.gov.au/dataset/12'
    e1 = ProvEntity(e1_label_string, e1_uri_string)

    e2_label_string = 'Input Entity 2'
    e2_uri_string = 'http://ecat.ga.gov.au/dataset/13'
    e2_value = 42
    e2 = ProvEntity(e2_label_string, e2_uri_string, None, None, e2_value)

    # handover Entity
    e_hand_label_string = 'Handover Entity'
    e_hand_uri_string = 'http://ecat.ga.gov.au/dataset/14'
    e_hand = ProvEntity(e_hand_label_string, e_hand_uri_string)

    # an output Entity
    e_out_label_string = 'Output Entity'
    e_out_uri_string = 'http://ecat.ga.gov.au/dataset/15'
    e_out = ProvEntity(e_out_label_string, e_out_uri_string)

    # the Report's starting Activity
    activity_uri_string = 'http://promsns.org/demo/abc-123'
    activity_label_string = 'Test Starting Activity'
    startedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    endedAtTime_date = datetime.strptime('2014-01-01T12:13:14', '%Y-%m-%dT%H:%M:%S')
    a_start = ProvActivity(
        activity_label_string,
        startedAtTime_date,
        endedAtTime_date,
        None,
        activity_uri_string,
        None,
        [e1, e2],
        [e_hand]
    )

    # the Report's ending Activity
    activity2_uri_string = 'http://promsns.org/demo/abc-124'
    activity2_label_string = 'Test Ending Activity'
    startedAtTime2_date = datetime.strptime('2014-01-01T12:14:14', '%Y-%m-%dT%H:%M:%S')
    endedAtTime2_date = datetime.strptime('2014-01-01T12:14:14', '%Y-%m-%dT%H:%M:%S')
    a_end = ProvActivity(
        activity2_label_string,
        startedAtTime2_date,
        endedAtTime2_date,
        None,
        activity2_uri_string,
        None,
        [e_hand],
        [e_out]
    )

    # the triples
    g.add((report_uri, RDF.type, PROMS.InternalReport))
    g.add((report_uri, RDFS.label, report_label))
    g.add((report_uri, PROMS.wasReportedBy, URIRef(wasReportedBy.uri)))
    g.add((report_uri, PROMS.startingActivity, URIRef(a_start.uri)))
    g.add((report_uri, PROMS.endingActivity, URIRef(a_end.uri)))
    g.add((report_uri, PROMS.nativeId, nativeId))
    g.add((report_uri, PROV.generatedAtTime, generatedAtTime))

    # add the Agent's graph
    g = g + wasReportedBy.get_graph()

    # add the Activities's graph
    g = g + a_start.get_graph()
    g = g + a_end.get_graph()

    # create a Report via toolkit, get its graph
    r = PromsInternalReport(
        report_label_string,
        wasReportedBy,
        nativeId_string,
        a_start,
        a_end,
        [a_start, a_end],
        generatedAtTime_date)

    g2 = r.get_graph()

    # replace the auto-assigned URI of the Report with the same one used for the hand made copy
    g2.update(
        '''
        PREFIX proms: <http://promsns.org/def/proms#>
        DELETE {
            ?s ?p ?o
        }
        INSERT {
            <''' + report_uri_string + '''> ?p ?o
        }
        WHERE {
            ?s a proms:InternalReport .
            ?s ?p ?o .
        }
        '''
    )

    assert g.isomorphic(g2)


if __name__ == '__main__':
    logging.basicConfig()

    test_report_basic_minimal()
    test_report_external_minimal()
    test_report_internal_minimal()
