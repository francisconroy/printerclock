import BaseHTTPServer
import random
import re

with open("template.html") as openedfile:
    template = openedfile.read()

class Server(BaseHTTPServer.BaseHTTPRequestHandler):
    def addfunc(self, funcin, *args):
        self.getfunc = funcin
        self.getfunc_args = args
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _post_return_dict(self, indata):
        regex=r"(.+)=(.+)"
        dict = {}
        for line in indata:
            print(line)
            result = re.match(regex, line)
            newkey = result.group(1)
            newvalue = result.group(2)
            dict[newkey] = newvalue
        return dict

    def do_GET(self):
        if not self.path.endswith('favicon.ico'):
            self._set_headers()
            ds = self.getfunc(*self.getfunc_args)
            if ds == 0:
                status = "closed"
                colour = "#f49241"
            else:
                status = "open"
                colour = "#42f47a"

            print("Command is:{}".format(self.path))
            print("Door State is:{}".format(status))
            self.wfile.write(template.format(status, colour))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        print("Response!")
        content_len = int(self.headers.getheader('Content-length', 0))
        print(self.headers)
        post_body = self.rfile.read(content_len)
        post_body = post_body.split('\n')

        print(post_body)
        # Do a thing
        result, name = self.postfunc(self._post_return_dict(post_body))
        self._set_headers()
        if result:
            self.wfile.write("<html><body><h1>Come on in {}!</h1></body></html>".format(name))
        else:
            self.wfile.write("<html><body><h1>Sorry, not sure who you are</h1></body></html>")

## Testing
def main():
    import auth
    ## Init auth
    configfile = auth.ConfigFile("userdata.txt")
    configfile.print_users()

    print("Starting testserver!")
    ## Web server config
    server_address = ('', 8000)

    print("Initialising the system...")
    handler_class = Server
    handler_class.getfunc = random.randint
    handler_class.getfunc_args = (0, 1)
    handler_class.postfunc = configfile.checkpin_from_dict
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    main()

