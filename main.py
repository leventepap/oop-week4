import datetime


def is_after(t1, t2):
    """Checks whether `t1` is after `t2`.

    >>> is_after(make_time(3, 2, 1), make_time(3, 2, 0))
    True
    >>> is_after(make_time(3, 2, 1), make_time(3, 2, 1))
    False
    >>> is_after(make_time(11, 12, 0), make_time(9, 40, 0))
    True
    """
    return None


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

first_date = Date(1933, 6, 22)
second_date = Date(1933, 9, 17)

def make_date(year, month, day):
    return Date(year, month, day)

def print_date(date):
    print(f"{date.year}-{date.month}-{date.day}")

def is_after_date(date1, date2):
    if date1.year > date2.year:
        return True
    elif date1.year < date2.year:
        return False
    elif date1.month > date2.month:
        return True
    elif date1.month < date2.month:
        return False
    elif date1.day > date2.day:
        return True
    return None