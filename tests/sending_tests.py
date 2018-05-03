import logging
from pyproms import *
import os
from datetime import datetime


def make_basic_report():
    # Example Agents, could be people or Organisations
    ag = ProvAgent("Agent Orange")
    agx = ProvAgent("Agent X")

    # A ReportingSystem (Agent subclass)
    # This is the system that actually generates the Reports
    rs = PromsReportingSystem('Workflow System Z')

    # The single Activity, as Basic Reports only allow 1
    startedAtTime = datetime.strptime('2014-06-25T12:13:14', '%Y-%m-%dT%H:%M:%S')
    endedAtTime = datetime.strptime('2014-06-25T12:13:24', '%Y-%m-%dT%H:%M:%S')
    report_activity = ProvActivity('Test Activity',
                                   startedAtTime,
                                   endedAtTime,
                                   wasAssociatedWith=agx,
                                   comment='A test Activity')
    generatedAtTime = datetime.strptime('2014-06-25T12:13:34', '%Y-%m-%dT%H:%M:%S')

    # make the Report
    r = PromsBasicReport('Test Basic Report PyPROMS',
                         rs,  # this is the Reporting System
                         'report-71',  # this could be anything that the Reporting System uses to keep track of Reports
                         report_activity,
                         generatedAtTime,
                         comment='This is an example Basic Report')

    return r


def test_report_send():
    rs = ReportSender()
    # post a report file
    r = rs.post(
        'http://52.64.5.57/proms/function/lodge-report',
        os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'examples', 'example_report_basic.ttl')
    )
    assert r.status_code == 201

    # post a Report object
    r = rs.post(
        'http://52.64.5.57/proms/function/lodge-report',
        make_basic_report()
    )
    assert r.status_code == 201


if __name__ == '__main__':
    logging.basicConfig()

    test_report_send()
