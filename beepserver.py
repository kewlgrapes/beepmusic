#!/usr/bin/python
"""
beepserver.py
  Nick Becker
  16 January, 2016
  HTTP frontend for beepmusic program.
  Access it at 127.0.0.1:8000 (by default).
"""
import logging
import sys
import threading
import BaseHTTPServer

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

class BeepHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  """
  Custom class to serve HTML pages to play beepmusic.
  """
  def do_HEAD(self):
    """
    Build and send HTTP header.
    """
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

  def do_GET(self):
    """
    Respond to an HTTP GET.
    """
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    print self.path

###########################################################
# main program
###########################################################

if __name__ == "__main__":
  # create the HTTP server
  httpd = BaseHTTPServer.HTTPServer((HOST, PORT), BeepHandler)
  t = threading.Thread(target=httpd.serve_forever)
  t.start()
  logging.info("beepserver running on %s:%d" % (HOST, PORT))

  # wait until the user presses Enter
  raw_input("Press Enter to terminate")
  logging.info("shutting down beepserver")
  httpd.shutdown()

