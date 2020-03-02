import json
import cgi
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse, request


class Server(BaseHTTPRequestHandler):

    @staticmethod
    def usd_to_rub_convert(usd: float):
        try:
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            rates = request.urlopen(url)
        except Exception as e:
            try:
                sys.stderr.write(f"request.urlopen error: url: {url}, msg: {e.msg}, code: {e.code}\n")
            except AttributeError:
                sys.stderr.write("connection error\n")
            return -1, -1, -1

        rates_json = json.loads(rates.read())
        rate_usd_to_rub = rates_json["Valute"]["USD"]["Value"]
        rub_value = round(usd * rate_usd_to_rub, 2)
        rate_update_date = rates_json["Date"]
        return rub_value, rate_update_date, round(rate_usd_to_rub, 2)

    def sent_convert_answer(self, value):
        rub_value, rate_update_date, rate_usd_to_rub = Server.usd_to_rub_convert(value)

        if (rub_value, rate_update_date, rate_usd_to_rub) == (-1, -1, -1):
            self.api_error("server_error: cannot get rate", 500)
        else:
            answer_json = {
                'currency_from': 'usd',
                'currency_to': 'rub',
                'rate_update_date': rate_update_date,
                'rate_source': 'www.cbr.ru',
                'value': value,
                'convert_rate': rate_usd_to_rub,
                'convert_value': rub_value
            }
            self._set_header()
            self.wfile.write((json.dumps(answer_json)).encode())
            sys.stderr.write(f"successfully converted\njson:{answer_json}\n")

    def api_error(self, error_message: str, http_status_code: int):
        self.send_response(http_status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write((json.dumps({'error_message': error_message})).encode())
        sys.stderr.write(f"error occurred: {error_message}\n")

    def _set_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # GET sends back a Hello world message
    def do_GET(self):

        url = parse.urlparse(self.path)

        if url.path != "/convert-usd-to-rub":
            self.api_error('invalid get request path', 400)
            return

        if url.query:
            params = dict(parse.parse_qsl(url.query))
        else:
            params = {}
        try:
            usd_value = float(params.get("usd"))
        except TypeError:
            self.api_error('invalid get request parameter', 400)
            return

        self.sent_convert_answer(usd_value)

    def do_POST(self):

        url = parse.urlparse(self.path)
        if url.path != "/convert-usd-to-rub":
            self.api_error('invalid post request path', 400)
            return

        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.api_error('non-json content', 400)
            return

        content = None
        if self.headers["Content-Length"]:
            length = int(self.headers["Content-Length"])
            content = self.rfile.read(length)
        info = None
        print(content)
        if content:
            try:
                info = json.loads(content)
            except:
                self.api_error('invalid json', 400)
                raise Exception("invalid json")
        else:
            self.api_error('invalid json', 400)
            return

        if info.get("currency_from") and info.get("currency_to") and info.get("value") is not None:
            if info.get("currency_from") == "usd" and info.get("currency_to") == "rub":
                value = info['value']
                if type(value) == str:
                    self.api_error('value must be numeric', 400)
                    return
                else:
                    self.sent_convert_answer(value)
            else:
                self.api_error('convert not support', 400)
                return
        else:
            self.api_error('invalid json', 400)
            return


def run(server_class=HTTPServer, handler_class=Server, addr="localhost", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
