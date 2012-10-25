#! /usr/bin/env python

import itertools
import os
import os.path
import time
from datetime import timedelta, datetime
import re
import optparse
from optparse import OptionParser
from collections import defaultdict

from date import *
from rcalendar import *
from printer import *

from settings import *

def parsedate(d):
    """Gets an input string (hopefully) representing a date
    and returns a datetime object for the respective datetime."""
    # auxiliary functions
    iden = lambda x:x
    def adjustY(da):
        return da.replace(year = datetime.today().year)
    # parse complete date string (including possibly duration)
    # according to certain regexp
    DATE_INPUT_RE = ["^(\d+)((\+\d+[mhd]?))?$"]
    a = None
    for rexp in DATE_INPUT_RE:
        a = re.match(rexp, d)
        if a is not None:
            break
    if a is None:
        return None
    # now we should have a combination of start date and duration
    startdate = a.group(1)
    DATE_INPUT_FORMATS = [("%Y%m%d", 
                           lambda x: (iden(x),True)), # 20121026  (date only)
                          ("%d.%m.%Y", 
                           lambda x: (iden(x),True)),  # 26.10.2012 (date only)
                          ("%Y%m%d%H%M", 
                           lambda x: (iden(x),False)),# 201210261930(datetime)
                          ("%m%d", 
                           lambda x: (adjustY(x), True)),# 1024     (no year)
                          ]
    result = None
    for (form, post) in DATE_INPUT_FORMATS:
        try:
            result = datetime(*(time.strptime(startdate, form)[0:6]))
            result = post(result)
            result, wholeday = result
        except:
            pass
        else:
            break
    td = timedelta(seconds=0)
    duration = defaultdict(lambda : 0)
    if a.group(2) is not None:
        duration[a.group(2)[-1]] = int(a.group(2)[:-1])
        td = timedelta(days=duration["d"],
                       hours=duration["h"],
                       minutes=duration["m"])
    return (result, result+td, wholeday)

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
    parser.add_option("-c", "--category",
                        action="store",
                        type="string",
                        dest="category",
                        default="")
    (options, args) = parser.parse_args()
    # positional arguments determine action
    if len(args)==0 or args[0]=="show" or args[0]=="s":
        cal = RCalendar(options.calendar_path)
        printdates(cal.dates)
    elif args[0]=="add" or args[0]=="a":
        (start, end, wholeday) = parsedate(args[1])
        print start, end
        d = Date(" ".join(args[2:]), start, end, wholeday=wholeday)
        f = open(options.calendar_path, "a")
        f.write(d.calendarstring())
        f.close()
        print d.calendarstring()

if __name__ == "__main__":
    main()
