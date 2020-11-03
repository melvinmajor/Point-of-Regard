#!/usr/bin/python3 -u
# coding=utf-8
import time
import datetime
import json
import sys
import logging
import logging.handlers
import argparse
import textwrap

DATA_FILE = 'data/Test Your Awareness eyes data.txt';
JSON_FILE = 'PoR-data.json';

''' arguments available to launch the app in a specific way '''
feature = argparse.ArgumentParser(prog='Data to JSON converter', add_help=True, prefix_chars='-', formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent('''\
        Point of Regard - Data to JSON converter module
        -----------------------------------------------
        This script is meant to be used in order to convert data to a suitable format, JSON.
        It takes necessary data from the original file and write a new one.
        '''))
feature.add_argument('-f', '--file', help='Path of the original file to convert', type=str, default=DATA_FILE, required=False)
feature.add_argument('-v', '--version', help='%(prog)s program version', action='version', version='%(prog)s v0.1')
args = feature.parse_args()

''' Log configuration '''
logger = logging.getLogger('PoR-data')
logger.setLevel(logging.INFO)
LOG_ROTATE = 'midnight'
# create a file handler and timed rotating
handler = logging.handlers.TimedRotatingFileHandler('PoR-data.log', when=LOG_ROTATE, utc=False)
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
alice = logging.StreamHandler()
alice.setFormatter(formatter)
logger.addHandler(alice)

# Fail method
def fail(msg):
    print(">>> Oops:",msg,file=sys.stderr)
    logger.warning('Oops: %s', msg)

# Method to check the presence of a JSON file
def checkJsonFile():
    try:
        with open(JSON_FILE) as json_data:
            data = json.load(json_data)
    except IOError as e:
        data = []
        fail('IOError while trying to open JSON file')
        raise


if __name__ == "__main__":
    while True:
        checkJsonFile()
    except (KeyboardInterrupt, SystemExit):
        logger.info('KeyboardInterrupt/SystemExit caught')
        sys.exit()

