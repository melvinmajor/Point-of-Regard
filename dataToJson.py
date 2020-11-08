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

data_path = "data/Test Your Awareness eyes data.txt";
JSON_FILE = "PoR-data.json";

''' arguments available to launch the app in a specific way '''
feature = argparse.ArgumentParser(prog='dataToJson.py', add_help=True, prefix_chars='-', formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent('''\
        Point of Regard - Data to JSON converter module
        -----------------------------------------------
        This script is meant to be used in order to convert data to a suitable format, JSON.
        It takes necessary data from the original file and write a new one.
        '''))
feature.add_argument('-f', '--file', help='Path of the original file to convert', type=str, default=data_path, required=False)
feature.add_argument('-v', '--version', help='%(prog)s program version', action='version', version='%(prog)s v0.1')
args = feature.parse_args()

if args.file:
    data_path = args.file

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

def converter(src, dst):
    logger.info('Source file path: %s', src)
    if args.file:
        logger.info('Exportation file name: %s', args.file)
    else:
        logger.info('Exportation file name: %s', dst)
    data = []
    try:
        with open(src, 'r') as f:
            #f.readlines()[2:]
            # Read each line and trims of extra spaces and gives only the valid words
            for line in f:
                value = list(line.strip().split())
                logger.debug(value)
                # Creating dictionary for each parameter
                temp_data = {
                        'time': value[0],
                        'type': value[1],
                        'LporX': value[21],
                        'LporY': value[22],
                        'RporX': value[23],
                        'RporY': value[24]
                }
                data.append(temp_data)
    except IOError as e:
        fail('IOError while trying to open and read source file')
        raise

    try:
        # Creating the JSON file
        with open(dst, 'w') as out_file:
            json.dump(data, out_file, indent = 2)
        out_file.close()
        logger.info('File has been successfully converted in JSON')
    except IOError as e:
        fail('IOError while trying to open and write destination file')
        raise


if __name__ == "__main__":
    try:
        fileSource = data_path
        fileDestination = JSON_FILE
        converter(fileSource, fileDestination)

    except (KeyboardInterrupt, SystemExit):
        logger.info('KeyboardInterrupt/SystemExit caught')
        sys.exit()

