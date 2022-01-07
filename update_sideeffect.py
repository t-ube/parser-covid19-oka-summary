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
            file_href = href
            find_file = file_name
            print('OK:'+find_file)
        elif 'hukuhan' in file_name:
            print('Find hukuhan')
            file_href = href
            find_file = file_name
            print('OK:'+find_file)
        elif 'kensuu' in file_name:
            print('Find kensuu')
            file_href = href
            find_file = file_name
            print('OK:'+find_file)
        else:
            print('Notfound key')


download_url = domain + file_href
newfilename = './pdf/sideeffect_' + find_file
urllib.request.urlretrieve(download_url, newfilename)
print("PDF downloaded at: pdf/" + find_file)

pdf = pdfplumber.open(newfilename)

#pdf = pdfplumber.open('./pdf/hukuhannou0914.pdf')

for page in pdf.pages:

    bounding_box = (420, 54, 540, 68)
    page_crop = page.within_bbox(bounding_box)
    page_crop.to_image(resolution=200).save("./snapshot/lastupdate_sideeffect.png", format="PNG")
    writedata['lastupdate'] = convertKanjiDateTime2En(page_crop.extract_text())
    
    tables = page.extract_tables({
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "intersection_y_tolerance": 1,
        "min_words_horizontal": 2,
    })

    for index,table in enumerate(tables):
        print(index)
        if index == 0:
            localDf = pd.DataFrame(table, columns=["pfizer_case", "pfizer_serious", "pfizer_dead", "moderna_case", "moderna_serious", "moderna_dead"])
            print(localDf)
            for index, row in localDf.iterrows():
                if index != 4:
                    print('index!=4')
                else:
                    writedata['pfizer_case'] = int(row['pfizer_case'])
                    writedata['pfizer_serious'] = int(row['pfizer_serious'])
                    writedata['pfizer_dead'] = int(row['pfizer_dead'])
                    writedata['moderna_case'] = int(row['moderna_case'])
                    writedata['moderna_serious'] = int(row['moderna_serious'])
                    writedata['moderna_dead'] = int(row['moderna_dead'])
        elif index == 1:
            localDf = pd.DataFrame(table, columns=["astrazeneca_case", "astrazeneca_serious", "astrazeneca_dead", "unknown_case", "unknown_serious", "unknown_dead"])
            print(localDf)
            for index, row in localDf.iterrows():
                if index != 4:
                    print('index!=4')
                else:
                    writedata['astrazeneca_case'] = int(row['astrazeneca_case'])
                    writedata['astrazeneca_serious'] = int(row['astrazeneca_serious'])
                    writedata['astrazeneca_dead'] = int(row['astrazeneca_dead'])
                    writedata['unknown_case'] = int(row['unknown_case'])
                    writedata['unknown_serious'] = int(row['unknown_serious'])
                    writedata['unknown_dead'] = int(row['unknown_dead'])
            
print(writedata)

# 情報の保存
update_wfile = open('./data/oka-sideeffect.json', 'w', encoding='utf8')
json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
update_wfile.close()
