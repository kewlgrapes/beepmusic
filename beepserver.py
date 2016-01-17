#!/usr/bin/python
"""
beepserver.py
  Nick Becker
  16 January, 2016
  HTTP frontend for beepmusic program.
  Access it at 127.0.0.1:8000 (by default).
"""
import logging
import os
import sys
import threading

from  BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from beepmusic import *

###########################################################
# constants/config
###########################################################

# where to run the HTTP server
HOST = "127.0.0.1"
PORT = 8000

###########################################################
# custom HTTP server
###########################################################

class BeepHandler(BaseHTTPRequestHandler):
  """
  Custom class to serve HTML pages to play beepmusic.
  """
  # map resource name to file location for HTTP GETS
  RESOURCES = {
    # HTML
    "/": (
      os.path.join(sys.path[0], "resources", "index.html"),
      "text/html"
    ),
    "/404.html": (
      os.path.join(sys.path[0], "resources", "404.html"),
      "text/html"
    ),
    "/500.html": (
      os.path.join(sys.path[0], "resources", "500.html"),
      "/text/html"
    ),
    "/index.html": (
      os.path.join(sys.path[0], "resources", "index.html"),
      "text/html"
    ),
    # JS
    "/beepmusic.js": (
      os.path.join(sys.path[0], "resources", "beepmusic.js"),
      "text/javascript"
    ),
    "/bootstrap.js": (
      os.path.join(sys.path[0], "resources", "bootstrap.js"),
      "text/javascript"
    ),
    "/jquery.js": (
      os.path.join(sys.path[0], "resources", "jquery.js"),
      "text/javascript"
    ),
    # CSS
    "/beepmusic.css": (
      os.path.join(sys.path[0], "resources", "beepmusic.css"),
      "text/css"
    ),
    "/bootstrap.css": (
      os.path.join(sys.path[0], "resources", "bootstrap.css"),
      "text/css"
    ),
    "/jumbotron-narrow.css": (
      os.path.join(sys.path[0], "resources", "jumbotron-narrow.css"),
      "text/css"
    )
  }

  # map resource name to python function for HTTP POSTS
  ACTIONS = {
  }
  
  def do_HEAD(self):
    """
    Build and send HTTP header.
    """
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

  def send_resource(self, code, data_type, data):
    """
    Build and send an  HTML header with the specified code,
    then send the resource data.
    """
    self.send_response(code)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(data)

  def do_GET(self):
    """
    Respond to an HTTP GET.
    """
    if not self.path in self.RESOURCES:
      print self.path
    try:
      if self.path in self.RESOURCES:
        # a known resource was requested
        r = self.RESOURCES[self.path]
        with open(r[0]) as f:
          self.send_resource(200, r[1], f.read())
        f.close()

      else: 
        # resource not found
        r = self.RESOURCES["/404.html"]
        with open(r[0]) as f:
          self.send_resource(404, r[1], f.read())
        f.close()

    except IOError as e:
      # hopefully the IO works this time...
      r = self.RESOURCES["/500.html"]
      with open(r[0]) as f:
        self.send_resource(500, r[1], f.read())
      f.close()

###########################################################
# main program
###########################################################

if __name__ == "__main__":
  # check that all resources exist
  try:
    for path, _ in BeepHandler.RESOURCES.values():
      assert os.path.exists(path)
  except AssertionError as e:
    logging.error("Resource does not exist at %s" % path)
    sys.exit(1)

  # start the server
  httpd = HTTPServer((HOST, PORT), BeepHandler)
  logging.info("beepserver running on %s:%d" % (HOST, PORT))
  httpd.serve_forever()
