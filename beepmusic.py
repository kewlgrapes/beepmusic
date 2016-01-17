#!/usr/bin/python
"""
beepmusic.py
  Nick becker
  14 August, 2015
  Play music through the motherboard speaker.
"""
import logging
import os
import re
import sys
import time

###########################################################
# constants
###########################################################

PITCHES = [0.00, 27.50, 29.14, 30.87, 32.70, 34.65, 36.71, 38.89, 41.20,
           43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74, 65.41, 69.30,
           73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54,
           123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00,
           196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.67,
           311.13, 329.63, 349.23, 370.00, 392.00, 415.31, 440.00, 466.16,
           493.88, 523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99,
           783.99, 830.61, 880.00, 932.33, 987.77, 1046.50, 1108.73,
           1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22,
           1760.00, 1864.66, 1975.53, 2093.00, 2217.46, 2349.31, 2489.02,
           2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31,
           3951.07, 4186.01]

PITCH_MIN = PITCHES[1] # PITCHES[0] is needed for the binary search
PITCH_MAX = PITCHES[-1]

COUNTS = {'s': 16, 'e': 8, 'q': 4, 'h': 2, 'w': 1}

BEEP_PATH = '/usr/bin/beep'

###########################################################
# exceptions
###########################################################

class PitchRangeException(Exception):
  pass

###########################################################
# functions
###########################################################

def beep(frequency, duration):
  """
  Make the pc speaker beep.
  Frequency in Hz, duration in milliseconds.
  """
  os.system('%s -f %.3f -l %d' % (BEEP_PATH, frequency, duration))

def pitch_index(frequency):
  """
  Returns the index in PITCHES of the nearest tone.
  """
  imin = 0
  imax = len(PITCHES)

  # binary search
  while imax - imin > 1:
    imid = int((imin + imax) / 2.0)
    if PITCHES[imid] < frequency:
      imin = int((imin + imax) / 2.0)
    else:
      imax = int((imin + imax) / 2.0)
  return imid

def pitch_offset(base, offset):
  """
  Returns the frequency offset from a base pitch by the given number
  of semitones.
  """
  return PITCHES[min(max(1, base + offset), len(PITCHES)-1)]

def calc_durations(tempo, style=None):
  """
  Calculate the note durations for sixteenth, eighth, quarter,
    half, and whole notes for the given tempo in the given style.
  Tempo is given in beats per minute.
  Durations are returned in milliseconds.
  """
  # duration of quarter note
  q = 60.0 / tempo
  return {'s': q * 250,
          'e': q * 500,
          'q': q * 1000,
          'h': q * 2000,
          'w': q * 4000}

def play(commands):
  """
  b{base}: set the base pitch to {base}
  t{tempo}: set the tempo to {tempo} bpm

  s{offset}: emit a tone {offset} semitones from {base} for 1/4 beat
  e{offset}: emit a tone {offset} semitones from {base} for 1/2 beat
  q{offset}: emit a tone {offset} semitones from {base} for 1 beats
  h{offset}: emit a tone {offset} semitones from {base} for 2 beats
  w{offset}: emit a tone {offset} semitones from {base} for 4 beats
  (s|e|q|h|w)r: per above, but rest for the specified number of beats

  #: comment (for duration of line)
  |: no action
  """
  # index of base pitch in PITCHES
  base = 0

  # note durations for 60 bpm
  duration = calc_durations(60)

  # group(0): entire match
  # group(1): (s|e|q|h|w)(.)({duration}|r)
  # group(2): s|e|q|h|w
  # group(3): .
  # group(4): {duration}|r
  # group(5): b|t({pitch}|{tempo})
  # group(6): b|t
  # group(7): {pitch}|{tempo}
  reg_command = re.compile(r'((s|e|q|h|w)(\.?)(-?\d+|r))|' # note or rest
                          + '((b|t)(-?\d+\.?\d*))')        # base or tempo

  # process the commands
  #logging.debug('\t' + '\t'.join([str(i) for i in range(8)]))
  for c in commands:
    m = reg_command.match(c)

    # no match
    if m is None:
      logging.warn('unable to handle command: %s' % c)
      continue
    #logging.debug('\t'.join([c] + [str(m.group(i)) for i in range(8)]))
    
    # note or rest?
    if not m.group(1) is None:
      # calculate duration (in milliseconds)
      d = duration[m.group(2)] 
      if m.group(3) == '.':
        d *= 1.5
      
      # rest
      if m.group(4) == 'r':
        logging.debug('rest for %.2f counts' % \
          (4.0 / COUNTS[m.group(2)] * (1.5 if m.group(3) else 1)))
        time.sleep(d / 1000.0)

      # note
      else:
        # note
        p = pitch_offset(base, int(m.group(4)))
        logging.debug('emit %.2f for %.2f counts' % \
          (p, 4.0 / COUNTS[m.group(2)] * (1.5 if m.group(3) else 1)))
        beep(p, d)
      
    # base?
    elif m.group(6) == 'b':
      base = pitch_index(float(m.group(7)))
      logging.debug('changed base frequency to %.2f' % PITCHES[base])

    # tempo?
    elif m.group(6) == 't':
      duration = calc_durations(float(m.group(7)))
      logging.debug('note durations set to: %s' % str(duration))

    # ?????
    else:
      logging.warn("this probably shouldn't happen")
  
###########################################################
# main program
###########################################################

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  
  # make sure input file is given
  if len(sys.argv) < 2:
    print 'usage: beepmusic <in_file>'
    sys.exit(1)
  in_file = sys.argv[1]

  # get list of commands
  try:
    with open(in_file, 'r') as f:
      logging.info('opened %s for reading' % in_file)
      lines = [l for l in f if not l.startswith('#')]
      logging.info('read %d lines from %s' % (len(lines), in_file))
    logging.info('closed %s' % in_file)
  except Exception as e:
    logging.error(str(e))
    sys.exit(1)

  # incomprehensible list comprehension
  commands = [w for words in [l.split() for l in lines] 
                for w in words if w != '|']
  logging.info('%s commands to process' % len(commands))

  # play some beautiful music
  play(commands)
