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



class Browser:
    options = Options()
    
    def __init__(self,driver_path=f"{os.getcwd()}\\chromedriver.exe",hide :bool =True):
        if hide: self.hide()
        else : pass
        self.s = Service(driver_path)
        self.driver = webdriver.Chrome(service = self.s,options=self.options) #create driver
        


    def hide(self):
        '''add arguments to hide windows'''
        self.options.add_argument("--headless") ##Use HeadLess Mode
        self.options.add_argument('--no-sandbox') 
        self.options.add_argument('--disable-gpu')  
        self.options.add_argument('log-level=3')  ##Hide Concole Warning/Errors 
        

    
    def download_path(self,path:str):
        '''choose download path instead of default path by check if path is valid or not then add experimental option that change download path of driver'''
        try: os.chdir(path)
        except: raise f"Please Enter Valid Path: {path} is not valid path"
        else: self.options.add_experimental_option("prefs",{'download.default_directory': path})

    def hide_ads(self):
        '''used to hide unwanted ad tab that auto apper when click on any element'''
        if len(self.driver.window_handles)>1: # check if there is more than one tab 
            self.driver.switch_to.window(self.driver.window_handles[-1]) #go to ad tab to close it
            time.sleep(3)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1]) #go back to egybest website

    def search(self,q:str):
        '''will call it to search for film_name and choose one of resulte on egybest'''
        search_box= self.driver.find_element(By.XPATH,'//*[@id="head"]/div/div[2]/form/input[2]') # define search_box element 
        time.sleep(2) #use it to make our programe as normal user and don't detect it
        search_box.send_keys(q,Keys.ENTER) #search for entered film_name
        self.hide_ads() #to hide appered ads
        
    def show_result(self):
        soup =bs(self.driver.page_source,'html.parser')
        self.results_title = soup.find_all('span',attrs={'class':'title'})
        rates = soup.find_all('i',attrs={"class":"i-fav rating"})
        ## Create Table
        table = PrettyTable()
        table.add_column('Index',column= range(1,len(self.results_title)))
        table.add_column('Result Title',column=[title.text for title in self.results_title])
        table.add_column('Rate',column=[rate.text for rate in rates])

    def select_result(self,user_input: int):
        self.selected_result = self.driver.find_element(By.PARTIAL_LINK_TEXT,self.films_names[user_input-1].text)
        self.selected_result.click()
        self.hide_ads()

    def is_series(self) -> bool:
        if self.driver.current_url.find('movie')>-1:
            return False
        else:
            return True
    
    
class Search:

    def __init__(self,q:str):
        '''will call it to search for film_name and choose one of resulte on egybest'''
        self.url = "https://giga.egybest.org/explore/?q="+q
        self.response = requests.get(self.url)
        soup =bs(self.response.content,'html.parser')
        self.results_title = soup.find_all('span',attrs={'class':'title'})
        self.link = soup.find_all('a',attrs={"class":"movie"})



    def print_result(self):
        table = PrettyTable(["Index","Film Name"])
        for i in range(len(self.results_title)):
            table.add_row([f"{i}",self.results_title[i].text])
        print(table)

    def get_result_link(self,index:int):
        return self.link[index].get("href")


class Movie():
    options = Options()
    def __init__(self,url,quality):
        self.s = Service(f"{os.getcwd()}\\chromedriver.exe")
        self.driver = webdriver.Chrome(service = self.s,options=self.options)
        self.url = url
        self.driver.get(url)
        self.info = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/div[1]/div[2]/div[2]").text
        self.name = self.driver.find_element(By.XPATH,'//*[@id="mainLoad"]/div[1]/div[1]/div/h1/span').text
        self.rate = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[5]/td[2]/strong/span").text
        self.duration = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[6]/td[2]").text
        qualities = self.driver.find_elements(By.XPATH,'//*[@id="watch_dl"]/table/tbody/tr/td[2]')
        size = self.driver.find_elements(By.XPATH,'//*[@id="watch_dl"]/table/tbody/tr/td[3]')
        self.quality_size={}
        for i in range(len(qualities)):
            self.quality_size[qualities[i].text] = size[i].text
        self.download(quality)
        print('helo')

    def get_size(self,quality):
        return self.quality_size[quality]

    def download(self,quality="SD 360p"):
        '''Valid Quality iS : Low 240p
                              SD 360p
                              SD 480p
                              HD 720p
                              Full HD 1080p'''

        self.driver.find_element(By.XPATH,f'//*[@id="watch_dl"]/table/tbody/tr[{list(self.quality_size.keys()).index(quality)+1}]/td[4]/a[2]').click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        try: self.driver.find_element(By.XPATH,'//*[@id="mainLoad"]/div/a')
        except: pass
        else:
            self.driver.find_element(By.XPATH,'//*[@id="mainLoad"]/div/a').click()
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.download(quality)


        try: self.driver.find_element(By.XPATH,'//*[@id="video"]/div[5]')
        except: pass
        else:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)
            self.driver.find_element(By.CSS_SELECTOR,'body').click()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)
            self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.source = self.driver.find_element(By.XPATH,'//*[@id="video_html5_api"]/source').get_attribute("src")
        self.driver.quit()
        


def download(url,quality):
    options = Options()
    options.add_argument("--headless") 
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-gpu')  
    options.add_argument('log-level=3')
    s = Service(f"{os.getcwd()}\\chromedriver.exe")
    driver = webdriver.Chrome(service = s,options=options)
    driver.get(url)
    NAME = driver.find_element(By.XPATH,'//*[@id="mainLoad"]/div[1]/div[1]/div/h1/span').text
    qualities = driver.find_elements(By.XPATH,'//*[@id="watch_dl"]/table/tbody/tr/td[2]')
    size = driver.find_elements(By.XPATH,'//*[@id="watch_dl"]/table/tbody/tr/td[3]')
    quality_size={}
    for i in range(len(qualities)):
        quality_size[qualities[i].text] = size[i].text

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
    SOURCE = driver.find_element(By.XPATH,'//*[@id="video_html5_api"]/source').get_attribute("src")
    if len(SOURCE)<260:
        download(url,quality)
    driver.quit()
    return [SOURCE,NAME]