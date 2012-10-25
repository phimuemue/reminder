from datetime import date

class Task:
    """A simple class for tasks, also a base-class for dates."""
    props = {}
    def __init__(self, name, date=date.today(), wholeday=False):
        self.wholeday = wholeday
        self.name = name
        self.date = date
    def __str__(self):
        return str(self.date) + " " + self.name
    def __getitem__(self, x):
        return self.props[x]
    def __setitem__(self, x, e):
        self.props[x] = e
    def calendarstring(self):
        """Returns a string that can be written to the calender file."""
        result = "t"
        result = result + self.date.strftime("%Y%m%d%H%m%s") + "##"
        result = result + self.name
        return result  

class Date(Task):
    """A simple class holding a date."""
    props = {}
    repetition = ""
    def __init__(self, name, date=date.today(), end=date.today(), wholeday=True, repetition=""):
        Task.__init__(self, name, date, wholeday)
        self.repetition = repetition
        self.end = end
    def calendarstring(self):
        """Returns a string that can be written to the calender file."""
        result = "d"
        result = result + self.date.strftime("%Y%m%d%H%M00") 
        result = result + self.end.strftime("%Y%m%d%H%M00") 
        if not self.repetition=="":
            result = result + "+" + self.repetition
        result = result + "##"
        result = result + self.name
        return result  
