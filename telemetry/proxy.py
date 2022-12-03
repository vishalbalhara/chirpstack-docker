#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler,HTTPServer
import argparse, os, random, sys, requests

from socketserver import ThreadingMixIn

# using zt ip address so that we don't have to change it much
servers = ['http://localhost:9090', 'http://10.147.17.212:9090']

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET(body=False)
        return
    
    def do_GET(self, body=True):
        sent = False
        good_response = None
        resp = None
        try:
            for server in servers:
                url = '{}{}'.format(server, self.path)
                req_header = self.parse_headers()

                print(req_header)
                print(url)
                resp = requests.get(url, headers=req_header, verify=False)
                if resp.status_code == 200:
                    good_response = resp
            if not good_response: 
                good_response = resp
                sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            msg = resp.text
            if body:
                self.wfile.write(msg.encode(encoding='UTF-8',errors='strict'))
            return
        finally:
            if not sent:
                self.send_error(404, 'error trying to proxy')
    
    def do_POST(self, body=True):
        good_response = None
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        req_header = self.parse_headers()
        for server in servers:
            url = '{}{}'.format(server, self.path)
            print(f"url: {url}")
            resp = requests.post(url, data=post_body, headers=req_header, verify=False)
            print(f"code: {resp.status_code}")
            if not good_response:
                good_response = resp
        self.send_response(good_response.status_code)
        self.send_resp_headers(good_response)
        # if body:
        #     self.wfile.write(resp.content)
        return

    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        #print ('Response Header')
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                #print (key, respheaders[key])
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Proxy HTTP requests')
    parser.add_argument('--port', dest='port', type=int, default=9999,
                        help='serve HTTP requests on specified port (default: random)')
    parser.add_argument('--hostname', dest='hostname', type=str, default='en.wikipedia.org',
                        help='hostname to be processd (default: en.wikipedia.org)')
    args = parser.parse_args(argv)
    return args

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main(argv=sys.argv[1:]):
    global hostname
    args = parse_args(argv)
    hostname = args.hostname
    print('http server is starting on {} port {}...'.format(args.hostname, args.port))
    server_address = ('127.0.0.1', args.port)
    httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running as reverse proxy')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
