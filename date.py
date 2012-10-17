from datetime import date

class Date:
    """A simple class holding a date."""
    props = {}
    def __init__(self, description, date=date.today()):
        self.description = description
        self.date = date
