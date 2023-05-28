from math import ceil

import Lib.MyCalendar

def create():
    """
    create object of MyCalendar class and start work it
    """
    test = Lib.MyCalendar.MyCalendar(icopath='../resources/icon.ico')
    test.start()
