import itertools

import settings 

def printdates(raw_dates):
    """Pretty-prints a list of dates with day, time, etc."""
    toprint = ["="*(settings.CONSOLE_WIDTH-1)]
    dates = sorted(raw_dates, key=lambda x:x.date.date())
    for day, group in itertools.groupby(dates, lambda x:x.date.date()):
        first = True
        for event in sorted(group, key=lambda x:x.date.time()):
            name = wordwrap(str(event.name), settings.TEXT_WIDTH)
            datestring = day.strftime(settings.DATE_FORMAT)
            tf = ["*"*settings.TIME_STRING_LENGTH, str(event.date.time())[:8]]
            toprint.append ("%s %s %s" % 
                            ([" "*settings.DATE_STRING_LENGTH, datestring][first], 
                             tf[event.wholeday],
                             name[0].strip()))
            for r in name[1:]:
                toprint.append(
                    " "*(settings.DATE_STRING_LENGTH+settings.TIME_STRING_LENGTH+2) + r.strip())
            first = False
        toprint.append("\n");
    toprint.append("="*(settings.CONSOLE_WIDTH-1))
    # TODO: The following is ugly, but it's too late for 
    #       me to find out the real bug.
    result = "\n".join(toprint)
    result = result.replace("\n\n", "\n")
    print result

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
