import itertools
import os
import os.path
import time
from datetime import timedelta, datetime

from date import *
from rcalendar import *

from settings import *

# parameters for pretty-print-output
CONSOLE_WIDTH = 80
DATE_STRING_LENGTH = 10
TIME_STRING_LENGTH = 8
TEXT_WIDTH = 80 - 10 - 1 - 8 - 1
DATE_FORMAT = "%d.%m.%Y"
SEPARATE_DAYS = True


def printdates(raw_dates):
    """Pretty-prints a list of dates with day, time, etc."""
    dates = sorted(raw_dates, key=lambda x:x.date.date())
    for day, group in itertools.groupby(dates, lambda x:x.date.date()):
        first = True
        if SEPARATE_DAYS:
            print ""
        for event in sorted(group, key=lambda x:x.date.time()):
            name = wordwrap(str(event.name), TEXT_WIDTH)
            datestring = day.strftime(DATE_FORMAT)
            tf = ["*"*TIME_STRING_LENGTH, str(event.date.time())[:8]]
            print "%s %s %s" % ([" "*DATE_STRING_LENGTH, datestring][first], 
                                tf[event.usetime],
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

initialize()
cal = RCalendar(CALENDAR_PATH)
printdates(cal.dates)

print parsedate("1011")
