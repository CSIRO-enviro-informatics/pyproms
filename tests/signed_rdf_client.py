__author__ = 'django'

import requests
import rsa
from binascii import hexlify


class Signed_report:

    report_url = "http://localhost:9000/"

    def __init(self,report_server_url):
        if report_server_url:
            report_url = report_server_url

    def get_pkcs_privatekey(self,user):
        privatekey_url = self.report_url+"api/privatekey"
        resp = requests.get(privatekey_url, data={}, auth=(user, ''))
        if resp.status_code == 200:
            private_key_pkcs = resp.content
            return private_key_pkcs

    def post_signed_report(self, message, user, private_key_pkcs):
        pkey = rsa.PrivateKey.load_pkcs1(private_key_pkcs)
        signed_message = hexlify(rsa.sign(message,pkey,'SHA-1'))
        signed_post_url = "http://localhost:9000/api/signedreport/"
        signed_data = {
            "report": message,
            "signedreport": signed_message
        }
        resp_signed = requests.post(signed_post_url, data=signed_data, auth=(user, ''))
        if resp_signed.status_code == 200:
            return resp_signed.content
        else:
            return {"Error": resp_signed.content}


if __name__ == '__main__':
    report_server_url = "http://localhost:9000/"

    signed_report_instance = Signed_report()
    pkcs_private_key = signed_report_instance.get_pkcs_privatekey('bai187')
    message = 'Hello, world'
    result = signed_report_instance.post_signed_report(message, 'bai187', pkcs_private_key)
    print(result)
