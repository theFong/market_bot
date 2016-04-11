from Stocks.Company import Company
from Stocks.Time import Time
from Stocks.Browser import Browser
import _operator
__author__ = 'AlecFong'
import requests
from bs4 import BeautifulSoup
import ystockquote
import time

url = "http://www.barchart.com/stocks/signals/top100"
loginMWurl = "https://id.marketwatch.com/access/50eb2d087826a77e5d000001/latest/login_standalone.html?url=http%3A%2F%2Fwww.marketwatch.com%2Fuser%2Flogin%2Fstatus"
loginWSSurl = "https://www.wallstreetsurvivor.com/login?ReturnUrl=%2fdashboard"
userMW =  "a99fong@gmail.com"
passcode = "thebot1"
userWSS = "Stock_Test"
CompanyList = []
BuyList = []


#this retrieves a list of company names
def getCompanies():
    r = requests.get(url)
    soup = BeautifulSoup(r._content)
    links = soup.find_all("a")
    count = 0
    for link in links:
        if "/quotes/stocks/" in link.get("href"):
            count+=1
            if(count%2!=0):
                c = Company(link.text)
                CompanyList.append(c)

#this sets price and change for company
def getPrice_Change():
    r = requests.get(url)
    soup = BeautifulSoup(r._content)
    last = soup.find_all("td")
    count = 0
    tempPrice = []
    tempChange = []
    for link in last:
        if (link.get("id") != None):
            count+=1
            if(count%2 != 0):
                tempPrice.append(link.text)
            else:
                tempChange.append(link.text)

    for i in range(len(tempPrice)):
        CompanyList[i].setPrice(tempPrice[i])
        CompanyList[i].setChange(tempChange[i])

#Sets opinions for company
def getOpinions():
    r = requests.get(url)
    soup = BeautifulSoup(r._content)
    opin = soup.find_all("span")
    count = 0
    temp_opinion = []
    temp_preopin = []
    temp_lwopin = []
    temp_lmopin = []
    for cont in opin:
        if "+" in cont.text or "-" in cont.text or "unch" in cont.text:
            count = 0
        else:
            if "Buy" in cont.text:
                if (count == 0):
                    temp_opinion.append(cont.text.split("%")[0])
                elif (count == 1):
                    temp_preopin.append(cont.text.split("%")[0])
                elif (count == 2):
                    temp_lwopin.append(cont.text.split("%")[0])
                elif (count == 3):
                    temp_lmopin.append(cont.text.split("%")[0])
                count+=1
            elif "Sell" in cont.text:
                if (count == 0):
                    temp_opinion.append(int("-"+cont.text.split("%")[0]))
                elif (count == 1):
                    temp_preopin.append(int("-"+cont.text.split("%")[0]))
                elif (count == 2):
                    temp_lwopin.append(int("-"+cont.text.split("%")[0]))
                elif (count == 3):
                    temp_lmopin.append(int("-"+cont.text.split("%")[0]))
                count+=1
            elif "Hold" in cont.text:
                if (count == 0):
                    temp_opinion.append(0)
                elif (count == 1):
                    temp_preopin.append(0)
                elif (count == 2):
                    temp_lwopin.append(0)
                elif (count == 3):
                    temp_lmopin.append(0)
                count+=1
    for i in range(len(CompanyList)):
        CompanyList[i].setOpinion(temp_opinion[i])
        CompanyList[i].setPreopin(temp_preopin[i])
        CompanyList[i].setLWopin(temp_lwopin[i])
        CompanyList[i].setLMopin(temp_lmopin[i])
        CompanyList[i].getScore()
    CompanyList.sort(key=_operator.attrgetter('score'), reverse=True)

def is_market_open(t):
    if(t.check_time_pst(6.5,13)):
        if(t.is_a_weekday()):

            if(t.is_holiday()):
                return True
    else:
        return False

def displaycompanies():
    for i in range(len(CompanyList)):
        print(CompanyList[i].name + " Price: " + str(CompanyList[i].price) + " Change: " + str(CompanyList[i].change))

def displayopinions():
    for i in range(len(CompanyList)):
        print(CompanyList[i].name + "\nToday's Opinion: " + str(CompanyList[i].opinion) + " Previous Opinion: "
              + str(CompanyList[i].preopin) + " Last Week's Opinion: " + str(CompanyList[i].lwopin)
              + "Last Month's Opinioin: " + str(CompanyList[i].lmopin))

mrFile = ''
def writeCompanyData():
    t = Time()
    date = t.get_year_month_day()
    time = t.get_pacific_time()
    mrFile = date+'|'+time
    writeFileName(mrFile)
    file = open(date+'|'+time,'w')
    for i in range(len(CompanyList)):
        company = CompanyList[i]
        file.write(company.name+' '+str(company.price)+' '+str(company.change)+' '+str(company.opinion)+' '+str(company.preopin)+' '
                   +str(company.lwopin)+' '+str(company.lmopin)+' '+str(company.score)+'\n')
    file.close()

def writeFileName(fileName):
    file = open('File Names','r+')
    pContent = file.read()
    file.seek(0,0)
    file.write(fileName.rstrip('\r\n')+'\n'+pContent)
    file.close()

def writeBuyList():
    t = Time()
    date = t.get_year_month_day()
    time = t.get_pacific_time()
    file = open('BL'+' '+date+'|'+time,'w')
    for i in range(len(BuyList)):
        company = BuyList[i]
        file.write(company.name+' '+str(company.price)+' '+str(company.change)+' '+str(company.opinion)+' '+str(company.preopin)+' '
                   +str(company.lwopin)+' '+str(company.lmopin)+' '+str(company.score)+'\n')

def writeResults(browser):
    t = Time()
    date = t.get_year_month_day()
    file = open('Results','a')
    overallGains = browser.get_overal_returns()
    time.sleep(3)
    dayGains = browser.get_today_gains()
    time.sleep(3)
    overallReturns = browser.get_overal_returns()
    time.sleep(3)
    file.write(date+'\n'+
               overallGains+' '+overallReturns+' '+dayGains+'\n')

def getBuyList():
    for i in range(10):
        BuyList.append(CompanyList[i])

def getShares(browser):
    netWorth = browser.get_net_worth()
    for comp in BuyList:
        comp.shares = int((float(netWorth.replace(',',''))/10.0)/float(comp.price))

def is_internet():
    try:
        _= requests.get('http://www.marketwatch.com/', timeout = 5)
        return False
    except requests.ConnectionError:
        # print("no internet")
        pass
    return True


def playMarket(t):
    #checks if market is open
    while(is_market_open(t)):
        #at 7:00 pst do following
        if(t.get_pacific_time()=="07:00:00"):
            #waits for internet connection
            print(t.get_pacific_time())
            while(is_internet()):
                pass
            getCompanies()
            getPrice_Change()
            getOpinions()
            writeCompanyData()
            getBuyList()
            writeBuyList()
            browser = Browser()
            browser.setUp(loginMWurl)
            browser.login_market_watch(userMW, passcode)
            getShares(browser)
            for comp in BuyList:
                browser.buyMW(comp.name,comp.shares)
                time.sleep(2)
            browser.tearDown()
        #at 12:30 pst do following
        if(t.get_pacific_time()=='12:30:00'):
            #waits for internet connection
            while(is_internet()):
                pass
            browser = Browser()
            browser.setUp(loginMWurl)
            browser.login_market_watch(userMW, passcode)
            browser.sellAll(len(BuyList))
            time.sleep(5)
            writeResults(browser)
            time.sleep(5)
            browser.tearDown()
            CompanyList.clear()
            BuyList.clear()

t = Time()
t.get_market_holidays()
while(True):
    playMarket(t)





