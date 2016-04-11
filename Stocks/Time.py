__author__ = 'AlecFong'
from datetime import datetime
from datetime import date
from pytz import timezone
import requests
from bs4 import BeautifulSoup

class Time:
    def get_year_month_day(self):
        ymd = "%Y-%m-%d"
        utctime = datetime.now(timezone('UTC'))
        date = utctime.astimezone(timezone('US/Pacific'))
        return date.strftime(ymd)

    def get_pacific_time(self):
        hms = "%H:%M:%S"
        utctime = datetime.now(timezone('UTC'))
        pacificnow = utctime.astimezone(timezone('US/Pacific'))
        return pacificnow.strftime(hms)

    def get_eastern_time(self):
        hms = "%H:%M:%S"
        utctime = datetime.now(timezone('UTC'))
        easternnow = utctime.astimezone(timezone('US/Eastern'))
        return easternnow.strftime(hms)

    def is_a_weekday(self):
        d = datetime.now()
        return d.isoweekday() in range(1,6)

    #6:00 == 6 & 1:00 == 13
    def check_time_pst(self, s, e):
        d = datetime.now()
        return d.hour*60+d.minute in range(int(s*60),int(e*60))

    def get_market_holidays(self):
        holidays = open('holidays','r')
        self.holidayList = []
        for line in holidays:
            h = line.split('-')
            day = date.strftime(datetime.strptime(h[2].rstrip('\n')+'-'+h[0]+'-'+h[1],'%Y-%m-%d'),'%Y-%m-%d')
            self.holidayList.append(day)
        holidays.close()


    def is_holiday(self):
        for i in self.holidayList:
            # print(i)
            if(i == date.strftime(date.today(),'%Y-%m-%d')):
                return False
        return True


        # r = requests.get("https://isthemarketopen.com/")
        # soup = BeautifulSoup(r._content)
        # find = soup.find_all("td")

        # if "Jan" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(1)+"-"+str(day)), '%Y-%m-%d')
        # elif "Feb" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(2)+"-"+str(day)), '%Y-%m-%d')
        # elif "march" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(3)+"-"+str(day)), '%Y-%m-%d')
        # elif "april" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(4)+"-"+str(day)), '%Y-%m-%d')
        # elif "may" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(5)+"-"+str(day)), '%Y-%m-%d')
        # elif "june" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(6)+"-"+str(day)), '%Y-%m-%d')
        # elif "july" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(7)+"-"+str(day)), '%Y-%m-%d')
        # elif "aug" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(8)+"-"+str(day)), '%Y-%m-%d')
        # elif "sep" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(9)+"-"+str(day)), '%Y-%m-%d')
        # elif "oct" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(10)+"-"+str(day)), '%Y-%m-%d')
        # elif "nov" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(11)+"-"+str(day)), '%Y-%m-%d')
        # elif "dec" in date.lower():
        #     self.holiday = datetime.strptime(str(str(year)+"-"+str(12)+"-"+str(day)), '%Y-%m-%d')
print()