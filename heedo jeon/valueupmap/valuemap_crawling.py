import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import env

if __name__ == "__main__": 
    df = pd.read_excel(env.EXCEL_PATH, encoding=env.DEFAULT_ENCODING)
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('lang=ko_KR')

    driver = webdriver.Chrome(env.CHROME_PATH, options=options)
    driver.implicitly_wait(3)

    URL = 'https://www.valueupmap.com/'
    rows_list = []
    fail_cnt = 0
    
    for i in range(len(df)):
        temp_dict = {}
        apt_address = df.iloc[i, 0]

        driver.get(URL)
        driver.find_element_by_xpath('//*[@id="search_input"]').send_keys(apt_address)
        driver.find_element_by_xpath('//*[@id="search_btn"]').click()
        driver.implicitly_wait(3)

        try:
            driver.find_element_by_xpath('//*[@id="jusoInfoBtn"]').click()
        except Exception as e:
            print(e)
            fail_cnt += 1
            temp_dict['주소'] = apt_address
            temp_dict['용도지역'] = None
            temp_dict['면적'] = None
            temp_dict['신축년도'] = None
            temp_dict['규모'] = None
            rows_list.apped(temp_dict)
            continue

        time.sleep(4)
        
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
        
        print(f"{i} >> {apt_address} {apt_usage_area} {apt_area} {apt_new_year} {apt_scale}")
        rows_list.append(temp_dict)

    print(f"성공 : {len(df) - fail_cnt}, 실패 : {fail_cnt}")
    df_result = pd.DataFrame(rows_list)
    df_result.to_csv('./result.csv', encoding=env.DEFAULT_ENCODING)