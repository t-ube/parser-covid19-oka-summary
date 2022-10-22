import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import re
import pdfplumber
import pandas as pd
import dummy_line_houdouteikyo as dummyLine
import datetime
import json


# 報道提供ファイルの第 n 報を見つける
def findDaiHouData(kanji_datetime):
    s = kanji_datetime.replace('\n', '')
    find_pattern = r"^第\s*(?P<hou>\d*)\s*報：令和\s*(?P<reiwa>\d*)\s*年\s*(?P<m>\d*)\s*月\s*(?P<d>\d*)\s*日.*"
    m = re.match(find_pattern, s)
    if m == None:
        return None
    replace_pattern = lambda date: str(int(m.group('reiwa'))+2018) + '-' + \
        date.group('m') + '-' + date.group('d')
    en_date = re.sub(find_pattern, replace_pattern, s)
    tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
    return {
        'hou': int(m.group('hou')),
        'year': int(m.group('reiwa'))+2018,
        'month': int(m.group('m')),
        'day': int(m.group('d')),
        'date': tdate.strftime('%Y-%m-%d')
    }


# 報道提供ファイルのダウンロード
def downloadHoudouFile(download_url,file_name):
    download_file = './pdf/' + file_name
    if os.path.isfile(download_file):
        print("CSV downloaded skip: csv/" + file_name)
    else:
        urllib.request.urlretrieve(download_url, download_file)
        print("CSV downloaded at: csv/" + file_name)
    return download_file


# 報道提供資料の1ページ目を解析する
def analizeHoudouFile(houdouFile):
    patient = 0
    hospitalize = 0
    wait = 0
    hotel = 0
    home = 0
    checkout = 0
    release = 0
    dead = 0
    severe = 0
    moderate = 0

    pdf = pdfplumber.open(houdouFile)
    for indexPage, page in enumerate(pdf.pages):
        if indexPage == 0:
            tables = page.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_y_tolerance": 1,
                "min_words_horizontal": 2,
            })
            for indexTable, table in enumerate(tables):
                if indexTable == 0:
                    localDf = pd.DataFrame(table)
                    for index, row in localDf.iterrows():
                        if index == 2:
                            patient = int(row[1].replace(',',''))
                elif indexTable == 4:
                    localDf = pd.DataFrame(table)
                    for index, row in localDf.iterrows():
                        if index == 2:
                            hospitalize = int(row[1].replace(',',''))
                            severe = int(row[2].replace(',',''))
                            moderate = int(row[3].replace(',',''))
                            hotel = int(row[4].replace(',',''))
                            home = int(row[5].replace(',',''))
                            wait = int(row[6].replace(',',''))
                            dead = int(row[7].replace(',',''))
                            checkout = 0
                            release = patient - hospitalize - hotel - home - wait

            return {
                'hospitalize': hospitalize,
                'wait': wait,
                'hotel': hotel,
                'home': home,
                'checkout': checkout,
                'release': release,
                'dead': dead,
                'patient': patient,
                'severe': severe,
                'moderate': moderate,
                'lastupdate': ''
            }
    return None


# 陽性者の公開日データを生成する
def makeOpenDateData():
    domain = 'https://www.pref.okinawa.lg.jp'
    url = domain + '/site/hoken/kansen/soumu/press/20200214_covid19_pr1.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    lis = soup.find_all('li')
    for li in lis:
        info = findDaiHouData(li.text)
        if info is not None and info['hou'] > 840:
            print(info)
            href = li.find('a').get('href')
            if href and ('houdouteikyo' in href or 'teikyoushiryo' in href) and 'pdf' in href:
                print(href)
                file_name = href.split("/")[-1]
                file_href = href
                download_url = domain + file_href
                houdouFile = downloadHoudouFile(download_url,file_name)
                data = analizeHoudouFile(houdouFile)
                if data == None:
                    print('ERROR')
                else:
                    data['lastupdate'] = info['date']
                    return data
    return None

writedata = makeOpenDateData()

# 情報の保存
if writedata is not None:
    update_wfile = open('./data/summary-oka.json', 'w', encoding='utf8')
    json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
    update_wfile.close()
