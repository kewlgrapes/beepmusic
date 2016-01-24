#!/usr/bin/python
"""
evil.py
  Nick Becker
  23 January, 2016
"""
import random
import time

from beepmusic import *

while 1:
  beep(random.randint(0, 20000), random.randint(50, 100))
