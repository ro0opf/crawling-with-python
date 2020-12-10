import pandas as pd
import requests
import time
import random

from bs4 import BeautifulSoup as BS

if __name__ == "__main__":
    df = pd.read_excel('./city_code.xlsx')

    url = "http://asil.kr/rts_m/contents/inc/data_area.jsp"
    headers = {"Referer" : "http://asil.kr/app/ranking.jsp"}
    rows_list = []
    rows_count = 1
    
    for i in df.index:
        sidoNm = df.iloc[i,1]
        sidoCode = str(df.iloc[i, 0])
        payload = {"area" : sidoCode}
        response = requests.get(url, params=payload, headers=headers).json()

        gugunCodeList = []


        for data in response:
            payload = {"apt" : "", "area" : data["seq"], "theme" : "max", "deal" : "1", "range" : "35", "sY" : "2020",
                    "sM" : "7", "sD" : "1", "eY" : "2020", "eM" : "12", "eD" : "1"}
            rankURL = "http://asil.kr/app/data/data_ranking.jsp"
            rankResponse = requests.get(rankURL, params=payload, headers=headers).json()
            minIdx = min(len(rankResponse), 1)
            time.sleep(random.uniform(0.1,0.5))

            for i in range(0, minIdx):
                mDict = {}
                dataList = rankResponse[i]
                mDict['city'] = sidoNm
                mDict['gugun'] = data["name"]
                mDict['dong'] = dataList["addr"].split(" ")[-1]
                mDict['ranking'] = dataList["idx"]
                mDict['apt'] = dataList["name"]
                mDict['price'] = dataList["price"]
                mDict['date'] = dataList["yyyymm"]
                mDict['PY'] = dataList["m2"]
                mDict['FL'] = dataList["floor"]
                
                mDict['latitude'] = dataList["lat"]
                mDict['longitude'] = dataList["lng"]

                aptCode = dataList["seq"]

                aptUrl = f"http://asil.kr/rts_m/contents/apt_info.jsp?os=pc&apt={aptCode}"

                aptResponse = requests.post(aptUrl).content
                soup = BS(aptResponse, 'html.parser')

                temp = soup.find(class_='bl_st1').find_all('li')
                
                tempText = temp[0].text
                mDict['address'] = tempText[tempText.find(':') + 2 : ]

                tempText = temp[1].text
                mDict['builtDate'] = tempText[tempText.find(':') + 2 : ]

                tempText = temp[2].text
                mDict['sedaesu'] = tempText[tempText.find(':') + 2 : ]

                rows_list.append(mDict)
                print(f"LOG >> ROW COUNT = {rows_count}, City Code = {sidoCode}, Area Code = {data['seq']}")
                rows_count += 1
                
    resultDf = pd.DataFrame(rows_list)
    resultDf.to_csv("./result_Bef2.csv", encoding="utf-8-sig")

