import BaseHTTPServer
import random

with open("template.html") as openedfile:
    template = openedfile.read()

class S(BaseHTTPServer.BaseHTTPRequestHandler):
    def addfunc(self, funcin):
        self.getfunc = funcin
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
            self.wfile.write(template.format(status))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

## Testing
def main():
    print("Starting testserver!")
    ## Web server config
    server_address = ('', 8000)

    print("Initialising the system...")
    handler_class = S
    handler_class.getfunc = random.randint(0, 1)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    main()

