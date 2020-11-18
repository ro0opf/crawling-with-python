import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

if __name__ == "__main__": 
    df = pd.read_excel("./광주_1억_결과.xlsx", encoding="utf-8-sig")
    driver = webdriver.Chrome('../../chromedriver87.exe')
    driver.implicitly_wait(3)

    URL = 'https://www.valueupmap.com/'
    rows_list = []
    
    #len(df)
    for i in range(5):
        temp_dict = {}
        apt_address = df.iloc[i, 0]

        driver.get(URL)
        driver.find_element_by_xpath('//*[@id="search_input"]').send_keys(apt_address)
        driver.find_element_by_xpath('//*[@id="search_btn"]').click()
        driver.implicitly_wait(3)

        driver.find_element_by_xpath('//*[@id="jusoInfoBtn"]').click()
        time.sleep(6)
        
        apt_usage_area = driver.find_element_by_xpath('/html/body/div[1]/div[12]/div/div[6]/div/div[18]/ul/li[3]/div/span[2]').text
        apt_area = driver.find_element_by_xpath('/html/body/div[1]/div[12]/div/div[6]/div/div[18]/ul/li[4]/div/span[2]').text
        apt_new_year = driver.find_element_by_xpath('/html/body/div[1]/div[12]/div/div[6]/div/div[20]/dl/dd[1]').text
        apt_scale = driver.find_element_by_xpath('/html/body/div[1]/div[12]/div/div[6]/div/div[20]/dl/dd[6]').text

        driver.find_element_by_xpath('//*[@id="dlNav"]/span').click()
        driver.implicitly_wait(5)
        temp_dict['주소'] = apt_address
        temp_dict['용도지역'] = apt_usage_area
        temp_dict['면적'] = apt_area
        temp_dict['신축년도'] = apt_new_year
        temp_dict['규모'] = apt_scale

        rows_list.append(temp_dict)
        
    df_result = pd.DataFrame(rows_list)
    df_result.to_csv('./result.csv', encoding="utf-8-sig")