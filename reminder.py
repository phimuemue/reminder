#! /usr/bin/env python

import itertools
import os
import os.path
import time
from datetime import timedelta, datetime

import optparse
from optparse import OptionParser

from date import *
from rcalendar import *
from printer import *

from settings import *

def initialize():
    """Retrieves some information about the environment, 
    and stores them into the specific vars. Also takes care of proper
    initialization of calendar files etc."""


def parsedate(d):
    """Gets an input string (hopefully) representing a date
    and returns a datetime object for the respective datetime."""
    iden = lambda x:x
    def adjustY(da):
        return da.replace(year = datetime.today().year)
    DATE_INPUT_FORMATS = [("%Y%m%d", iden),     # 20121026     (date only)
                          ("%d.%m.%Y", iden),   # 26.10.2012   (date only)
                          ("%Y%m%d%H%M", iden), # 201210261930 (date and time)
                          ("%m%d", adjustY),    # 1024         (no year)
                          ]
    result = None
    for (form, post) in DATE_INPUT_FORMATS:
        try:
            result = datetime(*(time.strptime(d, form)[0:6]))
            result = post(result)
        except:
            pass
        else:
            return result
    return None

def main():
    """The well-known main function."""
    # get terminal size and adjust printing parameters
    (rows, cols) = os.popen("stty size", "r").read().split()
    global CONSOLE_WIDTH, TEXT_WIDTH
    CONSOLE_WIDTH = int(cols) if int(cols)!=0 else 80
    TEXT_WIDTH = CONSOLE_WIDTH - DATE_STRING_LENGTH - TIME_STRING_LENGTH - 2
    # read command line arguments
    parser = OptionParser()
    parser.add_option("-f", "--file", 
                        action="store", 
                        type="string", 
                        dest="calendar_path",
                        default=CALENDAR_PATH)
    (options, args) = parser.parse_args()
    # positional arguments determine action
    if len(args)==0 or args[0]=="show" or args[0]=="s":
        cal = RCalendar(options.calendar_path)
        printdates(cal.dates)
    if args[0]=="add" or args[0]=="a":
        print parsedate(args[1])

if __name__ == "__main__":
    main()
