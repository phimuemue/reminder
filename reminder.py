import itertools
import os
import os.path
import time
from datetime import timedelta, datetime

from date import *

# parameters for pretty-print-output
CONSOLE_WIDTH = 80
DATE_STRING_LENGTH = 10
TIME_STRING_LENGTH = 8
TEXT_WIDTH = 80 - 10 - 1 - 8 - 1
DATE_FORMAT = "%d.%m.%Y"
SEPARATE_DAYS = True

# parameters for calendar files
CALENDAR_PATH = os.path.expanduser("~/Documents/reminder/default.reminder")
DATE_SAVED_FORMATS = ["%Y%m%d",      # format for date only
                      "%Y%m%d%H%M%S" # format for "everything"
                      ]

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

def extractdatefromcalendar(raw_date):
    """Expects the *raw* date part (i.e. with type-specification
    and +(y/w/d/number) and extracts the beginning and end and whether
    the time is considered or not."""
    date = raw_date[1:]
    date = date.split("+")[0]
    dsf = DATE_SAVED_FORMATS
    datelength = 8 if len(date)==16 else 14
    def makedate(d):
        print d
        dsfi = 0
        l = 8
        if len(d)==28:
            dsfi = 1
            l = 14
        mydsf = dsf[dsfi]
        r1 = datetime.fromtimestamp(time.mktime(time.strptime(d[:l],mydsf)))
        r2 = datetime.fromtimestamp(time.mktime(time.strptime(d[l:],mydsf)))
        return (r1, r2, not len(date)==16)
    return makedate(date)

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
        (s,e,usetime) = extractdatefromcalendar(dateinfo)
        if dateinfo[0]=="d":
            new = Date(parts[1], s, usetime=usetime)
            dates.append(new)
        elif dateinfo[1]=="t":
            new = Task(parts[1], s, usetime=usetime)
            tasks.append(new)
        else:
            print "Warning. Unknown category."
    return (sorted(dates, key=lambda x:x.date), tasks)

initialize()
cal = opencalendar(CALENDAR_PATH)[0]
printdates(cal)
# for d in cal:
#     print d.calendarstring()

print parsedate("1011")
