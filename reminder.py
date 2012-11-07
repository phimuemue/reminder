#! /usr/bin/env python

import itertools
import os
import os.path
import time
from datetime import timedelta
import re
import optparse
from optparse import OptionParser
from collections import defaultdict

from date import *
from rcalendar import *
from printer import *

import settings

def date_with_duration(a):
    """Takes a date with duration and returns two datetime objects,
    one for the start, one for the end, and whether it's a whole-day.
    a is assumed to be the proper result of a re.match."""
    start, wholeday = parse_single_date(a.group(1))
    td = timedelta(seconds=0)
    duration = defaultdict(lambda : 0)
    if a.group(2) is not None:
        duration[a.group(2)[-1]] = int(a.group(2)[:-1])
        td = timedelta(days=duration["d"],
                       hours=duration["h"],
                       minutes=duration["m"])
    return (start, start+td, wholeday)
    

def parse_single_date(d):
    """This takes a *single* date (without duration/repetition)
    and returns the proper datetime and whether it isa whole day."""
    # auxiliary functions
    iden = lambda x:x
    def adjustY(da):
        return da.replace(year = datetime.today().year)
    # actual stuff
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
            result = datetime(*(time.strptime(d, form)[0:6]))
            result = post(result)
        except:
            pass
        else:
            break
    return result

def parsedate(d):
    """Gets an input string (hopefully) representing a date
    and returns the following: Start date, end date, and whether it's a
    whole-day-event. If nothing is recognized, (None, None, False) is
    returned.
    
    I tried to support quite a range of possible date formats:

    20121010       Year, Month, Day, whole day event
    1.4.2012       Usual (german) spelling of dates, whole day
    201210131500   Day with specific time
    1005           Just a day (current year inserted)

    Moreover, the user can specify a time range. Up to now, only
    one kind of specification is allowed. A date (in one of the 
    above formats), followed by a "+"-sign, and then the duration,
    e.g:
    201210201500+2h (means starting at 15:00 o'clock, enduring 2 hours
    """
    if d is None:
        return (None, None, False)
    # parse complete date string (including possibly duration)
    # according to certain regexp
    DATE_INPUT_RE = [("^(\d+)((\+\d+[mhd]?))?$", date_with_duration), ]
    a = None
    for (rexp,post) in DATE_INPUT_RE:
        a = re.match(rexp, d)
        if a is not None:
            break
    if a is None:
        return None
    return post(a)
    # now we should have a combination of start date and duration
    
def main():
    """The well-known main function."""
    # get terminal size and adjust printing parameters
    (rows, cols) = os.popen("stty size", "r").read().split()
    #global CONSOLE_WIDTH, TEXT_WIDTH
    settings.CONSOLE_WIDTH = int(cols) if int(cols)!=0 else 80
    settings.TEXT_WIDTH = settings.CONSOLE_WIDTH - \
                          settings.DATE_STRING_LENGTH - \
                          settings.TIME_STRING_LENGTH - 2
    # read command line arguments
    parser = OptionParser()
    parser.add_option("-f", "--file", 
                        help="Specify a calendar file to open. Needs not to be specified.",
                        action="store", 
                        type="string", 
                        dest="calendar_path",
                        default=CALENDAR_PATH)
    parser.add_option("-c", "--category",
                        action="store",
                        type="string",
                        dest="category",
                        help="Specify a category for this event. Currently not supported.",
                        default="")
    parser.add_option("-p", "--place",
                        action="store",
                        type="string",
                        dest="place",
                        help="Specify where the event is going to take place. Not supported.",
                        default="")
    parser.add_option("--before",
                        action="store",
                        type="string",
                        dest="before",
                        help="Only use dates before a certain date.",
                        default=None)
    parser.add_option("--after",
                        action="store",
                        type="string",
                        dest="after",
                        help="Only use dates after a certain date.",
                        default=None)
    (options, args) = parser.parse_args()
    # positional arguments determine action
    if len(args)==0 or args[0]=="show" or args[0]=="s":
        cal = RCalendar(options.calendar_path)
        printdates(cal.dates(after=parsedate(options.after)[0],
                                before=parsedate(options.before)[0]))
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
