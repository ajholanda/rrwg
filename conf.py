"""Load the setting from configuration file.

"""
import configparser
import os
import sys

FILENAME = 'rrwg.conf'

config = configparser.ConfigParser()
if os.path.exists(FILENAME):
    config.read(FILENAME)
else:
    print('Please fill up a configuration file called "{}".'
          .format(FILENAME))
    print('See https://github.com/aholanda/rrwg/blob/main/rrwg.conf for an example.')
    sys.exit(-1)
