from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from prettytable import PrettyTable
import requests



class Search:
    '''search for movie to show  result in main window using beautifulsoup to make it faster'''
    def __init__(self,q:str):
        '''will call it to search for film_name and choose one of resulte on egybest'''
        self.url = "https://giga.egybest.org/explore/?q="+q
        self.response = requests.get(self.url)
        soup =bs(self.response.content,'html.parser')
        self.results_title = soup.find_all('span',attrs={'class':'title'})
        self.link = soup.find_all('a',attrs={"class":"movie"})

    def get_result_link(self,index:int):
        return self.link[index].get("href")



def download(url,quality):
    options = Options()
    # Hide The Browser and make it run in background 
    options.add_argument("--headless") 
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-gpu')  
    options.add_argument('log-level=3')
    s = Service(f"{os.getcwd()}\\chromedriver.exe")
    driver = webdriver.Chrome(service = s,options=options) #initialize Chrome driver
    driver.get(url) 
    NAME = driver.find_element(By.XPATH,'//*[@id="mainLoad"]/div[1]/div[1]/div/h1/span').text #get film name
    qualities = driver.find_elements(By.XPATH,'//*[@id="watch_dl"]/table/tbody/tr/td[2]') 
    size = driver.find_elements(By.XPATH,'//*[@id="watch_dl"]/table/tbody/tr/td[3]')
    quality_size={}
    for i in range(len(qualities)):
        quality_size[qualities[i].text] = size[i].text

    #skip ads that shown
    while True:
        driver.find_element(By.XPATH,f'//*[@id="watch_dl"]/table/tbody/tr[{list(quality_size.keys()).index(quality)+1}]/td[4]/a[2]').click()
        driver.switch_to.window(driver.window_handles[-1])
        try: driver.find_element(By.XPATH,'//*[@id="mainLoad"]/div/a')
        except: break
        else:
            driver.find_element(By.XPATH,'//*[@id="mainLoad"]/div/a').click()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

    while True:
        try: driver.find_element(By.XPATH,'//*[@id="video_html5_api"]/source')
        except: break
        else:
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR,'body').click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            driver.close()
    
    driver.switch_to.window(driver.window_handles[-1])
    SOURCE = driver.find_element(By.XPATH,'//*[@id="video_html5_api"]/source').get_attribute("src") #Get Video Source
    if len(SOURCE)<260:
        download(url,quality)
    driver.quit()
    return [SOURCE,NAME]