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
  beep(random.randint(50, 500), random.randint(1, 200))
  time.sleep(random.randint(0, 5) / 10)
