import requests
import urllib.request

from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import os
import json
import sys
import pdfplumber
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

writedata = {}
writedata['lastupdate'] = ''

def copyFile(FromName,ToName):
    if os.path.exists(FromName) == False:
        print('Not found: '+FromName)
        return False

    if os.path.exists(ToName):
        os.remove(ToName)
        print('copy file')

    shutil.copyfile(FromName,ToName)
    return True

def renameFile(FromName,ToName,Backup):
    if os.path.exists(FromName) == False:
        print('Not found: '+FromName)
        return False

    if os.path.exists(ToName):
        os.remove(Backup)
        os.rename(ToName,Backup)
        print('rename file')

    os.rename(FromName,ToName)
    return True

def convertKanjiDateTime2En(kanji_datetime):
    s = kanji_datetime.replace('\n', '')
    print(s)
    find_pattern = r".*令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日.*"
    
    replace_reiwa = lambda date: date.group('r')
    reiwa = re.sub(find_pattern, replace_reiwa, s)
    year = str(int(reiwa,10) + 2018)

    replace_pattern = lambda date: year + '-' + date.group('m') + '-' + date.group('d') + ' ' + '00:00:00'
    en_datetime = re.sub(find_pattern, replace_pattern, s)
    tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
    en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    return en_datetime

def convertDateTimeText2DateText(datetimeText):
    tdatetime = datetime.datetime.strptime(datetimeText, '%Y-%m-%d %H:%M:%S')
    return tdatetime.strftime('%Y/%m/%d')

# ファイルのダウンロード
domain = 'https://www.pref.okinawa.lg.jp'
url = domain + '/site/chijiko/kohokoryu/covid-19vaccine/sessyujokyo.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find(id="tmp_contents").find_all('a')

for link in links:
    href = link.get('href')
    if href and 'pdf' in href:
        file_name = href.split("/")[-1]
        print('Find pdf:'+file_name)
        if 'houkoku' in file_name:
            print('Find houkoku')
        elif 'hukuhan' in file_name:
            print('Find hukuhan')
        elif 'panf' in file_name:
            print('Find panf')
        else:
            file_href = href
            find_file = file_name
            print('OK:'+find_file)

download_url = domain + file_href
newfilename = './pdf/vrs_' + find_file
urllib.request.urlretrieve(download_url, newfilename)
print("PDF downloaded at: pdf/" + find_file)

pdf = pdfplumber.open(newfilename)

for page in pdf.pages:

    bounding_box = (410, 70, 510, 90)
    page_crop = page.within_bbox(bounding_box)
    page_crop.to_image(resolution=200).save("./snapshot/lastupdate_vrs.png", format="PNG")
    writedata['lastupdate'] = convertKanjiDateTime2En(page_crop.extract_text())
    
    tables = page.extract_tables({
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "intersection_y_tolerance": 1,
        "min_words_horizontal": 2,
    })

    for table in tables:
        df0 = pd.DataFrame(table, columns=["area", "populat", "once_cnt", "sec_cnt", "once_ratio", "sec_ratio","elder","elder_once_cnt", "elder_sec_cnt", "elder_once_ratio", "elder_sec_ratio"])

        df1 = df0.replace({'%':'',',':''},regex=True)

        df1['lastupdate'] = writedata['lastupdate']

        df_a = df1.set_index('area', drop=False)
        df_b = df1.set_index('area', drop=True)
        
        localDf_a = df_a.dropna(how='any')
        print(localDf_a)

        localDf_b = df_b.dropna(how='any')
        #print(localDf_a)
        #print(localDf_b.transpose())
        localDf_a.to_csv('./data/vrs-okinawa.csv',encoding="'utf-8-sig",index = False)
        localDf_b.transpose().to_csv('./data/area-vrs-okinawa.csv',encoding="'utf-8-sig",index = True)

