import selenium as selenium
import threading
from queue import Queue

__author__ = 'AlecFong'
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest
import time
from datetime import date
from datetime import datetime
from pytz import timezone
from Stocks.Time import Time
from Stocks.Browser import Browser

url = "http://www.barchart.com/stocks/signals/top100"
loginurl = "https://id.marketwatch.com/access/50eb2d087826a77e5d000001/latest/login_standalone.html?url=http%3A%2F%2Fwww.marketwatch.com%2Fuser%2Flogin%2Fstatus"

opinion = []
user =  "a99fong@gmail.com"
passcode = "thebot1"
def printOpinions(url):
    r = requests.get(url)
    soup = BeautifulSoup(r._content)
    opin = soup.find_all("span")
    for cont in opin:
        if "Buy" in cont.text:
            opinion.append(cont.text.split("%")[0])
            print(cont.text.split("%")[0])
        elif "Sell" in cont.text:
            opinion.append(int("-"+cont.text.split("%")[0]))
            print("-"+cont.text.split("%")[0])
        elif "Hold" in cont.text:
            opinion.append(0)
            print(0)

def getOpinions(url):
    r = requests.get(url)
    soup = BeautifulSoup(r._content)
    opin = soup.find_all("span")
    count = -1
    temp_opinion = []
    temp_preopin = []
    temp_lwopin = []
    temp_lmopin = []
    for cont in opin:
        count+=1
        if (count%4 == 0):
            count = 0
        if "Buy" in cont.text:
            if (count == 0):
                temp_opinion.append(cont.text.split("%")[0])
            elif (count == 1):
                temp_preopin.append(cont.text.split("%")[0])
            elif (count == 2):
                temp_lwopin.append(cont.text.split("%")[0])
            elif (count == 3):
                temp_lmopin.append(cont.text.split("%")[0])
        elif "Sell" in cont.text:
            if (count == 0):
                temp_opinion.append(int("-"+cont.text.split("%")[0]))
            elif (count == 1):
                temp_preopin.append(int("-"+cont.text.split("%")[0]))
            elif (count == 2):
                temp_lwopin.append(int("-"+cont.text.split("%")[0]))
            elif (count == 3):
                temp_lmopin.append(int("-"+cont.text.split("%")[0]))
        elif "Hold" in cont.text:
            if (count == 0):
                temp_opinion.append(0)
            elif (count == 1):
                temp_preopin.append(0)
            elif (count == 2):
                temp_lwopin.append(0)
            elif (count == 3):
                temp_lmopin.append(0)
    print(len(temp_opinion))
    print(len(temp_preopin))
    print(len(temp_lwopin))
    print(len(temp_lmopin))

#getOpinions(url)

#string = "Hold"
#l = string.split("%")
#print(l)
#if("Sell" in l[1]):
#    print(int("-"+l[0]))

def get_year_month_day():
    ymd = "%Y-%m-%d"
    utctime = datetime.now(timezone('UTC'))
    date = utctime.astimezone(timezone('US/Pacific'))
    print(date.strftime(ymd))

def get_pacific_time():
    hms = "%H:%M:%S"
    utctime = datetime.now(timezone('UTC'))
    pacificnow = utctime.astimezone(timezone('US/Pacific'))
    print(pacificnow.strftime(hms))

def get_eastern_time():
    hms = "%H:%M:%S"
    utctime = datetime.now(timezone('UTC'))
    easternnow = utctime.astimezone(timezone('US/Eastern'))
    print(easternnow.strftime(hms))
def is_a_weekday():
    d = datetime.now()
    return d.isoweekday() in range(1,6)

def check_time_pst():
    d = datetime.now()
    print(d.hour in range(6,13))

class LoginTest():

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(loginurl)

    def test_login(self):
        driver = self.driver
        userFieldID = "username"
        passFieldID = "password"
        loginbuttonXpath =  "//input[@value='Log In']"
        mwLogoXpath = "//a[@id='logo']"
        userFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(userFieldID))
        passFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID))
        loginButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(loginbuttonXpath))

        userFieldElement.clear()
        userFieldElement.send_keys(user)
        passFieldElement.clear()
        passFieldElement.send_keys(passcode)
        loginButtonElement.click()
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(mwLogoXpath))

    def tearDown(self):
        self.driver.quit()

def store_holiday():
    d = datetime.strptime('0001-1-1','%Y-%m-%d')
    r = requests.get("https://isthemarketopen.com/")
    soup = BeautifulSoup(r._content)
    find = soup.find_all("font")
    date = ""
    for link in find:
        if "clos" in link.text.lower():
            date = (link.text.split("-")[1][1:].lower())
    year = date.split(",")[1][1:]
    day = date[date.index(",")-2: date.index(",")]

    # if "jan" in date:
    #
    # elif "feb" in date:
    #
    # elif "april" in date:
    #
    # elif "may" in date:
    #
    # elif "june" in date:
    #
    if "july" in date.lower():
        d = datetime.strptime(str(year+"-"+str(7)+"-"+day), '%Y-%m-%d')
    # elif "aug" in date:
    #
    # elif "sep" in date:
    #
    # elif "oct" in date:
    #
    # elif "nov" in date:
    #
    # elif "dec" in date:
    print(d.strftime("%Y-%m-%d"))

# buylist = ["CHK","ALXN"]
# b = Browser()
# b.login_market_watch()

# count = 0
# while(True):
#     print(count)
#     time.sleep(2)
#     count+=1

def try_internet():
    try:
        _= requests.get('http://www.marketwatch.com/', timeout = 5)
        return False
    except requests.ConnectionError:
        pass
    return True

t = Time()
print(t.get_pacific_time())



# print_lock = threading.Lock()
#
# def exampleJob():
#     time.sleep(.5) # pretend to do some work.
#     with print_lock:
#         print(threading.current_thread().name)
#
# # The threader thread pulls an worker from the queue and processes it
# def threader():
#     while True:
#         # gets an worker from the queue
#         worker = q.get()
#
#         # Run the example job with the avail worker in queue (thread)
#         exampleJob()
#
#         # completed with the job
#         q.task_done()
#
# # Create the queue and threader
# q = Queue()
#
# # how many threads are we going to allow for
# for x in range(10):
#      t = threading.Thread(target=threader)
#
#      # classifying as a daemon, so they will die when the main dies
#      t.daemon = True
#
#      # begins, must come after daemon definition
#      t.start()
#
# start = time.time()
#
# # 20 jobs assigned.
# for worker in range(20):
#     q.put(worker)
#
# # wait until the thread terminates.
# q.join()
#
# # with 10 workers and 20 tasks, with each task being .5 seconds, then the completed job
# # is ~1 second using threading. Normally 20 tasks with .5 seconds each would take 10 seconds.
# print('Entire job took:',time.time() - start)
