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

from urlparse import parse_qs
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

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

  # map resource name to python function and parameter names for HTTP POSTS
  ACTIONS = {
    "beep": (
      beep,
      {"frequency": float, "duration":float}
    ),
    "pitch_index": (
      pitch_index,
      {"frequency": float}
    ),
    "pitch_offset": (
      pitch_offset,
      {"base": int, "offset": int}
    ),
    "play": (
      play,
      {"commands": list}
    )
  }
  
  def send_resource(self, code, data_type, data):
    """
    Build and send an  HTML header with the specified code,
    then send the resource data.
    """
    self.send_response(code)
    self.send_header("Content-type", data_type)
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
        logging.info("served %s" % self.path)

      else: 
        # resource not found
        r = self.RESOURCES["/404.html"]
        with open(r[0]) as f:
          self.send_resource(404, r[1], f.read())
        f.close()
        logging.warn("served /404.html")

    except IOError as e:
      # hopefully the IO works this time...
      r = self.RESOURCES["/500.html"]
      with open(r[0]) as f:
        self.send_resource(500, r[1], f.read())
      f.close()
      logging.error("served /500.html")

  def do_POST(self):
    """
    Respond to an HTTPD POST.
    """
    # parse the POST data
    content_length = int(self.headers["Content-Length"])
    post_data = parse_qs(self.rfile.read(content_length).decode("utf-8"))

    if "action" in post_data:
      if post_data["action"][0] in self.ACTIONS:
        # this is an action we can respond to
        a = self.ACTIONS[post_data["action"][0]]

        # reference to function to call
        f = a[0]

        # build kwargs and call function
        kwargs = {}
        for p, p_type in a[1].iteritems():
          if p in post_data:
            kwargs[p] = p_type(post_data[p][0])
        f(**kwargs)
        logging.info("responded to action: %s" % post_data["action"][0])
      else:
        logging.error("unknown action: %s" % post_data["action"])
    else:
      logging.error("malformed post_data: %s" % str(post_data))

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
