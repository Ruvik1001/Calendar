import calendar
import datetime
import logging
from tkinter import *


class MyCalendar:

    def __init__(self, title="Календарь", icopath='../resources/calendar.ico', holidaypath='../holi.txt'):
        """
        Class MyCalendar implements calendar with user-friendly interface
        :param title: liable of application
        :param icopath: path to icon of application
        :param holidaypath: path to file with holidays or where create it
        """
        f = open(holidaypath, 'a')
        f.close()

        self.root = Tk()
        self.root.title(title)
        self.root.resizable(False, False)
        self.days = []
        self.holidays = []

        self.now = datetime.datetime.now()
        self.year = self.now.year
        self.month = self.now.month

        self.back_button = Button(self.root, text="<", command=self._back)
        self.back_button.grid(row=0, column=0, sticky=NSEW)
        self.next_button = Button(self.root, text=">", command=self._next)
        self.next_button.grid(row=0, column=6, sticky=NSEW)

        self.add_hol_area = Text(self.root, width=10, height=1, bg='white',
                                 font=("Arial 16 bold", 12), fg='black', wrap=CHAR)
        self.add_hol_area.grid(row=9, column=2, columnspan=3, sticky=NSEW)
        self.add_hol_btn = Button(self.root, text="Add holiday", command=self._add_holi)
        self.add_hol_btn.grid(row=10, column=2, columnspan=3, sticky=NSEW)

        self.rem_hol_btn = Button(self.root, text="Remove holiday", command=self._rem_holi)
        self.rem_hol_btn.grid(row=11, column=2, columnspan=3, sticky=NSEW)

        self.info_label = Label(self.root, text='0', width=1, height=1, font='Arial 16 bold', fg='blue')
        self.info_label.grid(row=0, column=1, columnspan=5, sticky=NSEW)

        try:
            self.root.iconbitmap(icopath)
        except:
            logging.error("Ico not found...")

        self.holipath = holidaypath
        self._fill()

    def _back(self):
        """
        return calendar to prev month
        :return: void
        """
        self.month -= 1

        if self.month == 0:
            self.month = 12
            self.year -= 1

        self._fill()

    def _next(self):
        """
        return calendar to next month
        :return: void
        """
        self.month += 1

        if self.month == 13:
            self.month = 1
            self.year += 1

        self._fill()

    def _fill(self):
        """
        fill all square with data and coloring it
        :return: void
        """
        self.add_hol_area.delete('1.0', END)
        self.days.clear()
        self._reload_holidays()

        for n in range(7):
            lbl = Label(self.root, text=calendar.day_abbr[n], width=1, height=1, font='Arial 10 bold', fg='darkblue')
            lbl.grid(row=1, column=n, sticky=NSEW)

        for row in range(6):
            for col in range(7):
                if col == 5 or col == 6:
                    lbl = Label(self.root, text='0', width=4, height=2, font='Arial 16 bold', bg='red')
                else:
                    lbl = Label(self.root, text='0', width=4, height=2, font='Arial 16 bold')
                lbl.grid(row=row + 2, column=col, sticky=NSEW)
                self.days.append(lbl)

        self.info_label['text'] = calendar.month_name[self.month] + ',' + str(self.year)
        month_days = calendar.monthrange(self.year, self.month)[1]

        if self.month == 1:
            back_monts_days = calendar.monthrange(self.year - 1, 12)[1]
        else:
            back_monts_days = calendar.monthrange(self.year, self.month - 1)[1]

        week_day = calendar.monthrange(self.year, self.month)[0]

        for n in range(month_days):
            self.days[week_day + n]['text'] = n + 1
            self.days[week_day + n]['fg'] = 'black'
            if self.year == self.now.year and self.month == self.now.month and n == self.now.day - 1:
                self.days[week_day + n]['bg'] = 'green'
            else:
                if self.days[week_day + n]['bg'] == 'red':
                    continue
                else:
                    self.days[week_day + n]['bg'] = '#d2d2d2'

        for elem in self.holidays:
            if int(elem[0]) == self.month and self.days[week_day + int(elem[1]) - 1]['bg'] != 'green':
                self.days[week_day + int(elem[1]) - 1]['bg'] = 'red'

        for n in range(week_day):
            self.days[week_day - n - 1]['text'] = back_monts_days - n
            self.days[week_day - n - 1]['fg'] = 'grey'
            if self.days[week_day - n - 1]['bg'] == 'red':
                self.days[week_day - n - 1]['bg'] = '#a10000'
                continue
            self.days[week_day - n - 1]['bg'] = '#f3f3f3'

        for elem in self.holidays:
            if int(elem[0]) == self.month - 1 and week_day - back_monts_days + int(elem[1]) - 1 > -1:
                self.days[week_day - back_monts_days + int(elem[1]) - 1]['bg'] = '#a10000'

        for n in range(6 * 7 - month_days - week_day):
            self.days[week_day + n + month_days]['text'] = n + 1
            if self.days[week_day + n + month_days]['bg'] == 'red':
                self.days[week_day + n + month_days]['bg'] = '#a10000'
                continue
            self.days[week_day + n + month_days]['fg'] = 'grey'
            self.days[week_day + n + month_days]['bg'] = '#f3f3f3'

        for elem in self.holidays:
            if int(elem[0]) == self.month + 1 and (month_days + int(elem[1]) < 6 * 7):
                self.days[month_days + int(elem[1]) + 1]['bg'] = '#a10000'

        self.add_hol_area.insert(END, "дд.мм (напр: 01.01)")

    def start(self):
        """
        loading interface and start it in mainloop
        :return: void
        """
        self.root.mainloop()

    def _reload_holidays(self):
        """
        reload holidays
        :return: void
        """
        self.holidays.clear()
        f = open(self.holipath, 'r')
        for elem in f:
            if elem == '\n':
                break
            month, days = elem.split(sep='.')
            self.holidays.append([month, days])
        f.close()

    def _add_holi(self):
        """
        add new holidays in list
        :return: void
        """
        date = ''.join(char for char in self.add_hol_area.get('1.0', END) if char.isalnum() or char == '.')
        if len(date) != 5 or date[2] != '.' or str(date[0:2] + date[3:5]).isnumeric() == False:
            return

        f = open(self.holipath, 'a')
        f.write(date[3:5] + '.' + date[0:2] + '\n')
        f.close()
        self._fill()

    def _rem_holi(self):
        """
        rem holidays in list
        :return: void
        """
        date = ''.join(char for char in self.add_hol_area.get('1.0', END) if char.isalnum() or char == '.')
        if len(date) != 5 or date[2] != '.' or str(date[0:2] + date[3:5]).isnumeric() == False:
            return

        date = date[3:5] + '.' + date[0:2]
        f = open(self.holipath, 'r')
        f2 = open(str(self.holipath + 't'), 'w')

        for s in f:
            if s[:5] == date[:5]:
                continue
            f2.write(s + '\n')

        f.close()
        f2.close()
        f = open(self.holipath, 'w')
        f2 = open(str(self.holipath + 't'), 'r')

        for s in f2:
            f.write(s + '\n')

        f2.close()
        f.close()
        self._fill()
