from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import ssl

class CloudFlareExampleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # check if we are accessing the secure part of the page. block everything not coming from loopback
        if (self.path == '/secure'):
            if (self.request.getpeername()[0] == '127.0.0.1'):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('You are now in the secure part!', 'UTF-8'))
            else:
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        # else show all request headers
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.headers))

if __name__ == "__main__":
    hostName = input("Enter hostname []: ") or ""
    serverPort = int(input("Enter port [443]: ") or "443")
    handler = CloudFlareExampleServer

    with TCPServer((hostName, serverPort), handler) as httpd:
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile='/etc/letsencrypt/live/angseus.io/fullchain.pem', keyfile='/etc/letsencrypt/live/angseus.io/privkey.pem', server_side=True)
        print("Server started https://%s:%s" % (hostName, serverPort))

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

        httpd.server_close()
        print("Server stopped.")
