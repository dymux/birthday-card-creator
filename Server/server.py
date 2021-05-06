from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from urllib.parse import parse_qs
from urllib.parse import unquote
from tickets_db import TicketsDB
import random
import json

class MyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.cookie = cookies.SimpleCookie()
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin",self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials","true")
        self.send_cookie()
        BaseHTTPRequestHandler.end_headers(self)

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie",morsel.OutputString())

    def do_OPTIONS(self):
        self.load_cookie()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.load_cookie()
        if self.path == "/tickets":
            self.handleTicketsRetrieveCollection()
        else:
            self.handleNotFound()

    def do_POST(self):
        self.load_cookie()
        if "oompa" in self.cookie:
            self.handleForbidden()
            return
        if self.path == "/tickets":
            self.handleTicketsCreateMember()
        else:
            self.handleNotFound()

    def handleTicketsRetrieveCollection(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        db = TicketsDB()
        tickets = db.getTickets()
        self.wfile.write(bytes(json.dumps(tickets), "utf-8"))

    def handleTicketsCreateMember(self):
        self.cookie["oompa"] = "loompa"
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)

        entrant_name = parsed_body["entrant_name"][0]
        entrant_age = parsed_body["entrant_age"][0]
        guest_name = parsed_body["guest_name"][0]
        token = self.getRandomToken()

        db = TicketsDB()
        db.insertTicket(token, entrant_name, entrant_age, guest_name)

        self.send_response(201)
        self.end_headers()


    def handleNotFound(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("It seems that this resource has been lost in the chocolate pipes. An Oompa Loompa will be dispatched promptly to recover the artifact.", "utf-8"))

    def handleForbidden(self):
        self.send_response(403)
        self.end_headers()
        self.wfile.write(bytes("The Oompa Loompas have already recieved your ticket. Please try again tomorrow.", "utf-8"))

    def getRandomToken(self):
        return random.randint(0, 6)
def run():
  listen = ("127.0.0.1", 8080)
  server = HTTPServer(listen, MyRequestHandler)

  print("Listening...")
  server.serve_forever()

run()
