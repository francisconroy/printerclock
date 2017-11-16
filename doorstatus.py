import RPi.GPIO as GPIO
import BaseHTTPServer

template = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Testpage</title>
  <meta name="description" content="The HTML5 Herald">
  <meta name="author" content="SitePoint">
</head>

<body>
    {}
</body>
</html>
"""


def check_door_status(pindict):
    return GPIO.input(pindict['doorpin'])


pin_dict = {'doorpin': 12}
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_dict['doorpin'], GPIO.IN)


class S(BaseHTTPServer.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        ds = check_door_status(pin_dict)
        if ds == 0:
            status = "closed"
        else:
            status = "open"

        print("Command is:{}".format(self.command))
        print("Door State is:{}".format(status))
        self.wfile.write(template.format("<h1>Door is {}</h1>".format(status)))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

server_address = ('', 80)
handler_class = S


server_class = BaseHTTPServer.HTTPServer
httpd = server_class(server_address, handler_class)
httpd.serve_forever()