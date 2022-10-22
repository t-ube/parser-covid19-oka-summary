import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import re
import pdfplumber
import pandas as pd
import dummy_line_houdouteikyo as dummyLine
import datetime
import gc

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

# 報道提供資料をフォーマットする
def formatedHoudouFileTypeA(houdouFile):
    dummyLine.output_dummy_typeA('./component/dummy_line_houdouteikyo.pdf')
    dummyLine.output_mergePDF('./component/dummy_line_houdouteikyo.pdf',
        houdouFile, './pdf/processed_houdouteikyo.pdf')
    return './pdf/processed_houdouteikyo.pdf'

# 報道提供資料をフォーマットする
def formatedHoudouFileTypeB(houdouFile):
    dummyLine.output_dummy_typeB('./component/dummy_line_houdouteikyo.pdf')
    dummyLine.output_mergePDF('./component/dummy_line_houdouteikyo.pdf',
        houdouFile, './pdf/processed_houdouteikyo.pdf')
    return './pdf/processed_houdouteikyo.pdf'

# 報道提供資料をフォーマットする
def formatedHoudouFileTypeC(houdouFile):
    dummyLine.output_dummy_typeC('./component/dummy_line_houdouteikyo.pdf')
    dummyLine.output_mergePDF('./component/dummy_line_houdouteikyo.pdf',
        houdouFile, './pdf/processed_houdouteikyo.pdf')
    return './pdf/processed_houdouteikyo.pdf'

# 報道提供資料をフォーマットする
def formatedHoudouFileTypeD(houdouFile):
    dummyLine.output_dummy_typeD('./component/dummy_line_houdouteikyo.pdf')
    dummyLine.output_mergePDF('./component/dummy_line_houdouteikyo.pdf',
        houdouFile, './pdf/processed_houdouteikyo.pdf')
    return './pdf/processed_houdouteikyo.pdf'


# 報道提供資料の2ページ目以降を解析する
def analizeHoudouFile(houdouFile):
    minNumber = 999999999
    maxNumber = 0
    pdf = pdfplumber.open(houdouFile)
    for indexPage, page in enumerate(pdf.pages):
        tables = page.extract_tables({
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "intersection_y_tolerance": 1,
            "min_words_horizontal": 2,
        })
        for table in tables:
            localDf = pd.DataFrame(table)
            for index, row in localDf.iterrows():
                if index == 0 and row[0] != '確定陽性者':
                    return None
                if row[0] == '確定陽性者':
                    continue
                if 400000 > int(row[0]):
                    return None
                if int(row[0]) >= 1000000:
                    minNumber = min(int(row[0]), minNumber)
                    maxNumber = max(int(row[0]), maxNumber)
    return {'min': minNumber, 'max': maxNumber}

# 陽性者の公開日データを生成する
def makeOpenDateData(dest):
    domain = 'https://www.pref.okinawa.lg.jp'
    url = domain + '/site/hoken/kansen/soumu/press/20200214_covid19_pr1.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    lis = soup.find_all('li')
    df = pd.DataFrame(None,columns = ['opendate' , 'first_case', 'last_case'])
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
                data = analizeHoudouFile(formatedHoudouFileTypeA(houdouFile))
                if data == None:
                    data = analizeHoudouFile(formatedHoudouFileTypeB(houdouFile))
                    if data == None:
                        data = analizeHoudouFile(formatedHoudouFileTypeC(houdouFile))
                        if data == None:
                            data = analizeHoudouFile(formatedHoudouFileTypeD(houdouFile))
                            if data == None:
                                print('ERROR')
                if data != None:
                    df = df.append({'opendate': info['date'], 'first_case': data['min'], 'last_case': data['max']}, ignore_index=True)
                    print(data)

    df.to_csv(dest, encoding='utf_8_sig',index=False)
    del df
    gc.collect()

# make new opendate csv
makeOpenDateData('./csv/patients_opendate_r040927.csv')
