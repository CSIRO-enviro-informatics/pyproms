import os
import requests
from pyproms.proms_report import PromsReport
from rdflib import Graph, util


class ReportSender:
    """
    A tiny class to send Reports to a PROMS Server instance.
    Basically wraps requests post method
    """

    def post(self, proms_report_lodging_uri, report):
        """
        POSTS an RDF-serialised Report object to a PROMS server instance

        :param proms_report_lodging_uri: the URI of the PROMS server instance's Report lodgement endpoint.
        Typically something like {PROMS_URI}/function/lodge-report.
        :param report: a pyproms Report class object, an rdflib Graph of a Report, a Report file path or a string
        containing RDF of a Report in turtle

        :return: a requests module Response class
        """

        if isinstance(report, PromsReport):
            report_str = report.serialize_graph().decode('utf-8')
        elif isinstance(report, Graph):
            report_str = report.serialize(format='turtle')
        elif isinstance(report, str):
            if os.path.exists(report):
                g = Graph()
                g.parse(report, format=util.guess_format(report))
                report_str = g.serialize(format='turtle')
            else:  # assume it's an RDF string in turtle
                report_str = report
        else:  # don't allow anything else
            raise ValueError(
                'Only PromsReport objects, rdflib  Graph objects, path strings to RDF files or a string of '
                'RDF in turtle format are allowd for \'report\''
            )

        # POST the Report to PROMS
        headers = {'Content-type': 'text/turtle'}
        r = requests.post(proms_report_lodging_uri, data=report_str, headers=headers)

        return r
