import os
import os.path
import time
from datetime import timedelta, datetime

from settings import *

from date import *

def extractdatefromcalendar(raw_date):
    """Expects the *raw* date part (i.e. with type-specification
    and +(y/w/d/number) and extracts the beginning and end and whether
    the time is considered or not."""
    date = raw_date[1:]
    date = date.split("+")[0]
    dsf = DATE_SAVED_FORMATS
    datelength = 8 if len(date)==16 else 14
    def makedate(d):
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

class RCalendar:
    dates = []
    tasks = []
    def __init__(self, path):
        """Opens a calendar file and returns a sorted array of dates and
        an array of tasks.
        If the file is not present, it will be created. So do non-existent
        intermediate (sub)dirs on the way to the file."""
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
                self.dates.append(new)
            elif dateinfo[1]=="t":
                new = Task(parts[1], s, usetime=usetime)
                self.tasks.append(new)
            else:
                print "Warning. Unknown category."

