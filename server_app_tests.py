import json
import cgi
import sys

import unittest
import threading  # for tests
import requests  # for tests

from urllib import parse, request
from http.server import BaseHTTPRequestHandler, HTTPServer

from server_app import Server

server_class = HTTPServer
handler_class = Server
addr = "localhost"
port = 8085
server_address = (addr, port)
httpd = server_class(server_address, handler_class)


class TestRest(unittest.TestCase):

    def test_get_basic1(self):
        # correct get request
        try:
            threading.Thread(target=httpd.serve_forever).start()
            response = requests.get(url="http://127.0.0.1:8085/convert-usd-to-rub", params={"usd": "1"})
            print(response.headers['content-type'])
            self.assertEqual(response.headers['content-type'], "application/json")
            self.assertEqual(response.status_code, 200)
            httpd.shutdown()
        finally:
            pass

    def test_get_basic2(self):
        # invalid get request: get request without parameter "usd"
        try:
            threading.Thread(target=httpd.serve_forever).start()
            response = requests.get(url="http://127.0.0.1:8085/convert-usd-to-rub", params={})
            self.assertEqual(response.headers['content-type'], "application/json")
            self.assertEqual(response.status_code, 400)
            httpd.shutdown()
        finally:
            pass

    def test_post_basic1(self):
        # correct post request
        try:
            threading.Thread(target=httpd.serve_forever).start()
            data = {"currency_from": "usd", "currency_to": "rub", "value": 1.3}
            headers = {'content-type': 'application/json'}
            response = requests.post(url="http://127.0.0.1:8085/convert-usd-to-rub",
                                     data=json.dumps(data),
                                     headers=headers)
            self.assertEqual(response.headers['content-type'], "application/json")
            self.assertEqual(response.status_code, 200)
            httpd.shutdown()
        finally:
            pass

    def test_post_basic2(self):
        # invalid post request: post request usd to eur
        try:
            threading.Thread(target=httpd.serve_forever).start()
            data = {"currency_from": "usd", "currency_to": "eur", "value": 1.3}
            headers = {'content-type': 'application/json'}
            response = requests.post(url="http://127.0.0.1:8085/convert-usd-to-rub",
                                     data=json.dumps(data),
                                     headers=headers)
            self.assertEqual(response.headers['content-type'], "application/json")
            self.assertEqual(response.status_code, 400)
            httpd.shutdown()
        finally:
            pass


print(__name__)

if __name__ == "__main__":
    unittest.main()
