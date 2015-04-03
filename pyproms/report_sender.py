import requests


class ReportSender:
    """
    A tiny class to send Reports to a PROMS Server instance.
    Basically wraps requests post method
    """

    def post(self, report_register_uri, report):
        """
        POSTS an RDF-serialised Report object to a PROMS server instance

        :param report_register_uri: the URI of the PROMS server instance's Report register.
        :param report: a pyproms Report class object

        :return: a requests module Response class
        """
        #ensure Reports register has a trailing slash
        if not report_register_uri.endswith('/'):
            report_register_uri += '/'

        report_str = report.serialize_graph().decode('utf-8')

        #POST the Report to PROMS
        headers = {'Content-type': 'text/turtle'}
        r = requests.post(report_register_uri, data=report_str, headers=headers)

        return r
