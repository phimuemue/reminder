import itertools

from settings import *

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
