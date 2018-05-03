import requests


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
        :param report: a pyproms Report class object

        :return: a requests module Response class
        """

        report_str = report.serialize_graph().decode('utf-8')

        # POST the Report to PROMS
        headers = {'Content-type': 'text/turtle'}
        r = requests.post(proms_report_lodging_uri, data=report_str, headers=headers)

        return r
