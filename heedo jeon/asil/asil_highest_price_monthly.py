import pandas as pd
import requests
import time
import random
import env
import numpy as np
from bs4 import BeautifulSoup as BS

def getCalcYear(year, month):
    return year + ((month) // 12)

def getCalcMonth(month):
    res = (month + 1) % 12

    if res == 0:
        return 12
    return res

def getDiff(startYear, startMonth, endYear, endMonth):
    res = 0

    if startMonth > endMonth:
        res += endMonth + 12 - startMonth
        res += (endYear - 1 - startYear) * 12
    else:
        res += endMonth - startMonth
        res += (endYear - startYear) * 12
    return res + 1

def parsePrice(value: str):
    res = 0
    value = value.replace(",", "").replace("천","000").replace("만", "").replace(" ", "")

    idx = value.find("억")

    if idx != -1:
        res += int(value[:idx]) * 10000
        if idx + 1 != len(value):
            res += int(value[idx + 1:])
    else:
        res += int(value)
    
    return res

if __name__ == "__main__":
    df = pd.read_excel(env.CITY_CODE_PATH)

    url = "http://asil.kr/rts_m/contents/inc/data_area.jsp"
    headers = {"Referer": "http://asil.kr/app/ranking.jsp"}
    rows_list = []
    rows_count = 1

    startDate = input("시작년월을 입력하세요 (YYYYMM) : ")
    endDate = input("종료년월을 입력하세요 (YYYYMM) : ")

    startYear = int(startDate[:4])
    startMonth = int(startDate[4:])
    endYear = int(endDate[:4])
    endMonth = int(endDate[4:])

    for i in df.index:
        sidoNm = df.iloc[i, 1]
        sidoCode = str(df.iloc[i, 0])
        payload = {"area": sidoCode}
        gugunList = requests.get(url, params=payload, headers=headers).json()

        for gugun in gugunList:
            currYear = startYear
            currMonth = startMonth

            for diff in range(getDiff(startYear, startMonth, endYear, endMonth)):
                payload = {"apt": "", "area": gugun["seq"], "theme": "max", "deal": "1", "range": "35",
                           "sY": currYear, "sM": currMonth, "sD": "1", "eY": currYear, "eM": currMonth, "eD": "31"}
                rankURL = "http://asil.kr/app/data/data_ranking.jsp"
                rankResponse = requests.get(
                    rankURL, params=payload, headers=headers).json()

                # time.sleep(random.uniform(0.1, 0.5))
                mDict = {}
                try:
                    dataList = rankResponse[0]
                    mDict['city'] = sidoNm
                    mDict['gugun'] = gugun["name"]
                    mDict['price'] = parsePrice(dataList["price"])
                    mDict['date'] = f"{currYear}.{currMonth}"

                    rows_list.append(mDict)
                    print(f"LOG >> ROW COUNT = {rows_count}, City Code = {sidoCode} Date = {currYear}.{currMonth}")
                except Exception as e:
                    print(f"Error 발생 : {e}")
                    print(f"{gugun['name']}, Date = {currYear}.{currMonth}")
                finally:
                    rows_count += 1
                    currYear = getCalcYear(currYear, currMonth)
                    currMonth = getCalcMonth(currMonth)

    resultDf = pd.DataFrame(rows_list)
    resultDf = resultDf.pivot_table(
        index=['city', 'gugun'], columns='date', values='price', aggfunc=np.sum, fill_value=0)
    resultDf.to_csv("./result.csv", encoding="utf-8-sig")
