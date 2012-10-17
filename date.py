from datetime import date

class Date:
    """A simple class holding a date."""
    props = {}
    def __init__(self, description, date=date.today()):
        self.description = description
        self.date = date
    def __str__(self):
        return str(self.date) + " " + self.description
    def __getitem__(self, x):
        return self.props[x]
    def __setitem__(self, x, e):
        self.props[x] = e

