import itertools
import os

from date import *

CONSOLE_WIDTH = 80
DATE_STRING_LENGTH = 10
TIME_STRING_LENGTH = 8
TEXT_WIDTH = 80 - 10 - 1 - 8 - 1

def printdates(dates):
    """Pretty-prints a list of dates with day, time, etc."""
    for day, group in itertools.groupby(dates, lambda x:x.date.date()):
        first = True
        for event in sorted(group, key=lambda x:x.date.time()):
            description = wordwrap(str(event.description), TEXT_WIDTH)
            print "%s %s %s" % ([" "*DATE_STRING_LENGTH ,str(day)][first], 
                                str(event.date.time())[:8],
                                description[0].strip())
            for r in description[1:]:
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
           for i in xrange(20)]

initialize()
printdates(mydates)

for i in (wordwrap("Is there a way in python to programmatically determine the width of the console? I mean the number of characters that fits in one line without wrapping, not the pixel width of the window.", 50)):
    print i
