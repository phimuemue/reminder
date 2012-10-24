import os

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
