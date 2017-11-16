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

class S(BaseHTTPServer.BaseHTTPRequestHandler):
    def getstat_mock(self):
        return 1
    def __init__(self):
        self.getfunc = self.getstat_mock()
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if not self.path.endswith('favicon.ico'):
            self._set_headers()
            ds = self.getfunc
            if ds == 0:
                status = "closed"
            else:
                status = "open"

            print("Command is:{}".format(self.path))
            print("Door State is:{}".format(status))
            self.wfile.write(template.format("<h1>Door is {}</h1>".format(status)))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")