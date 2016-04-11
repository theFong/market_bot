from selenium.webdriver import ActionChains

__author__ = 'AlecFong'
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common import action_chains, keys
import time

class Browser:

    def setUp(self, url):
        self.driver = webdriver.Firefox()
        self.driver.get(url)

    def login_market_watch(self, user, passcode):
        driver = self.driver
        userFieldID = "username"
        passFieldID = "password"
        loginbuttonXpath = "//input[@value='Log In']"
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

    def login_wallstreetsurvivor(self, user, passcode):
        driver = self.driver
        userFieldID = "LoginModel_UserName"
        passFieldID = "LoginModel_Password"
        loginbuttonXpath = ".//*[@id='login_btn']"
        userFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(userFieldID))
        passFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID))
        loginButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(loginbuttonXpath))

        userFieldElement.clear()
        userFieldElement.send_keys(user)
        passFieldElement.clear()
        passFieldElement.send_keys(passcode)
        loginButtonElement.click()

    def buyMW(self, company, amount):
        #go to trade website
        self.driver.get("http://www.marketwatch.com/game/alecfongtest2/trade")
        driver = self.driver
        #get Xpath
        companyFieldXpath = ".//*[@id='fakemaincontent']/section/div[1]/div/input"
        searchbuttonXpath = ".//*[@id='fakemaincontent']/section/div[1]/div/button"
        #initialize elements
        compFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(companyFieldXpath))
        searchButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(searchbuttonXpath))

        compFieldElement.clear()
        #enter company symbol
        compFieldElement.send_keys(company)
        #click to search
        searchButtonElement.click()

        tradeFieldXpath = ".//*[@id='fakemaincontent']/section/div[2]/div/div[3]/div/button[2]"
        tradeFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(tradeFieldXpath))
        #click to trade
        tradeFieldElement.click()

        shareamountXpath = "//input[@value='0']"
        submittradeXpath = ".//*[@id='submitorder']/button"
        shareamountElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(shareamountXpath))
        submittradeElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(submittradeXpath))

        shareamountElement.clear()
        shareamountElement.send_keys(str(amount))
        submittradeElement.click()

    #not currently functioning
    def buyWSS(self, company, amount):
        #self.driver.get("http://www.wallstreetsurvivor.com/dashboard")
        driver = self.driver
        companyFieldID = "stock_trade_search_field"
        searchcompanyFieldXpath = "//button[@id='stock_trade_search_submit']"
        companyFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(companyFieldID))
        searchcompanyFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(searchcompanyFieldXpath))
        #addcompFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(addcompFieldXpath))

        companyFieldElement.clear()
        companyFieldElement.send_keys(company)
        add = driver.find_element_by_xpath("//a[contains(text(),'Add')]")
        ActionChains(driver).move_to_element(add).click().perform()


    def sellMW(self, company, buylist, amount):
        self.driver.get("http://www.marketwatch.com/game/alecfongtest2/portfolio/Holdings")
        driver = self.driver
        companysellbutXpath = ".//*[@id='maincontent']/section[2]/div[1]/table/tbody/tr[1]/td[7]/button"
        submitsaleXpath = "//div[3]/button"
        sortbysymbolXpath = "//a[contains(text(),'Symbol')]"
        shareamountXpath = "//div[@id='order']/div/div/div[2]/div/div/a/input"
        companysellbutElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(companysellbutXpath))
        submitsaleElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(submitsaleXpath))
        sortbysymbolElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(sortbysymbolXpath))
        shareamountElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(shareamountXpath))
        if(company < buylist[0] or company < buylist[1]):
            companysellbutElement.click()
            time.sleep(2)
            shareamountElement.clear()
            shareamountElement.send_keys(amount)
            submitsaleElement.click()
        else:
            sortbysymbolElement.click()
            time.sleep(2)
            companysellbutElement.click()
            time.sleep(2)
            shareamountElement.clear()
            shareamountElement.send_keys(amount)
            submitsaleElement.click()

    def sellAll(self, compNum):
        self.driver.get("http://www.marketwatch.com/game/alecfongtest2/portfolio/Holdings")
        driver = self.driver
        companysellbutXpath = ".//*[@id='maincontent']/section[2]/div[1]/table/tbody/tr[1]/td[7]/button"
        submitsaleXpath = "//div[3]/button" #".//*[@id='submitorder']/button"
        # exitSaleXpath = './/*[@id=\'popSTOCKXASQFIT\']/header/div'
        # exitSaleElement =  WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(exitSaleXpath))
        for comps in range(compNum):
            companysellbutElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(companysellbutXpath))
            submitsaleElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(submitsaleXpath))
            companysellbutElement.click()
            time.sleep(2)
            submitsaleElement.click()
            time.sleep(2)
            self.driver.get("http://www.marketwatch.com/game/alecfongtest2/portfolio/Holdings")

    def get_net_worth(self):
        self.driver.get("http://www.marketwatch.com/game/alecfongtest2/portfolio/Holdings")
        driver = self.driver
        return driver.find_element_by_xpath("//div[@id='maincontent']/section/div[2]/ul/li/span[2]").text[1:]

    def get_overall_gains(self):
        self.driver.get("http://www.marketwatch.com/game/alecfongtest1/portfolio/Holdings")
        driver = self.driver
        gains = driver.find_element_by_xpath("//div[@id='maincontent']/section/div[2]/ul/li[2]/span[2]").text
        return gains.replace("$","")

    def get_overal_returns(self):
        """"
        returns percentages(%)
        """
        self.driver.get("http://www.marketwatch.com/game/alecfongtest2/portfolio/Holdings")
        driver = self.driver
        returns = driver.find_element_by_xpath("//div[@id='maincontent']/section/div[2]/ul/li[3]/span[2]").text
        return returns.replace("%","")
    def get_today_gains(self):
        """"
        returns percentages(%)
        """
        self.driver.get("http://www.marketwatch.com/game/alecfongtest2/portfolio/Holdings")
        driver = self.driver
        returns = driver.find_element_by_xpath("//div[@id='maincontent']/section/div[2]/ul/li[4]/span[2]").text
        return returns.replace("%","")

    def tearDown(self):
        self.driver.quit()