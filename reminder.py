import itertools
import os
import os.path

from date import *

# parameters for pretty-print-output
CONSOLE_WIDTH = 80
DATE_STRING_LENGTH = 10
TIME_STRING_LENGTH = 8
TEXT_WIDTH = 80 - 10 - 1 - 8 - 1
DATE_FORMAT = "%d.%m.%Y"

# parameters for calendar files
CALENDAR_PATH = os.path.expanduser("~/Documents/reminder/default.reminder")
DATE_SAVED_FORMATS = ["%Y%m%d",     # format for date only
                      ]
DATE_INPUT_FORMATS = ["%Y%m%d",     # 20121026     (date only)
                      "%d.%m.%Y",   # 26.10.2012   (date only)
                      "%Y%m%d%H%M", # 201210261930 (date and time)
                      ]

def printdates(raw_dates):
    """Pretty-prints a list of dates with day, time, etc."""
    dates = sorted(raw_dates, key=lambda x:x.date.date())
    for day, group in itertools.groupby(dates, lambda x:x.date.date()):
        first = True
        for event in sorted(group, key=lambda x:x.date.time()):
            name = wordwrap(str(event.name), TEXT_WIDTH)
            datestring = datetime.strftime(day,DATE_FORMAT)
            print "%s %s %s" % ([" "*DATE_STRING_LENGTH, datestring][first], 
                                str(event.date.time())[:8],
                                name[0].strip())
            for r in name[1:]:
                print " "*(DATE_STRING_LENGTH+TIME_STRING_LENGTH+2) + r.strip()
            first = False

def wordwrap(string, width):
    """Takes a string and returns an array holding the single lines
    that look "good" for the specified width"""
    res = [""]
    for word in string.split():
        if len(res[-1]) + len(word) < width:
            res[-1] = res[-1] + word + " "
        elif len(word) >= width:
            res.append(word + " ")
            res.append("")
        else:
            res.append(word + " ")
    return res

def initialize():
    """Retrieves some information about the environment, 
    and stores them into the specific vars. Also takes care of proper
    initialization of calendar files etc."""
    (rows, cols) = os.popen("stty size", "r").read().split()
    global CONSOLE_WIDTH, TEXT_WIDTH
    CONSOLE_WIDTH = int(cols) if int(cols)!=0 else 80
    TEXT_WIDTH = CONSOLE_WIDTH - DATE_STRING_LENGTH - TIME_STRING_LENGTH - 2
    opencalendar(CALENDAR_PATH)

def opencalendar(path):
    """Opens a calendar file and returns a sorted array of dates and
    an array of tasks."""
    caldir = os.path.dirname(path)
    if not os.path.exists(caldir):
        print caldir + " does not exist. Creating it."
        os.makedirs(caldir)
    if not os.path.exists(path):
        print path + " does not exist. Creating it."
        f = open(path, "w")
        f.close()
        return []
    # here the important part
    f = open(path, "r")
    dates = []
    tasks = []
    for line in f:
        parts = line.split("##")
        dateinfo = parts[0]
        new = Date(parts[1], date=date)

# ================================ test stuff



import random
from random import randrange
from datetime import timedelta, datetime

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second))

mydates = [Date("date " + str(i) + "".join([random.choice("abcdefgh  ") for _ in xrange(200)]), 
                random_date(datetime.today(),datetime.today()+timedelta(2))) 
           for i in xrange(5)]

initialize()
printdates(mydates)

