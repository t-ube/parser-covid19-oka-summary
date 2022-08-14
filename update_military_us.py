from numpy import empty
import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import os
import pathlib
import json
import sys
import pdfplumber
import resize_pdf_us
import dummy_line_us

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
    s = kanji_datetime.replace('　',' ').replace('：',':').replace('（','')
    find_pattern = r"令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日 (?P<H>\d*):.*"
    m = re.search(find_pattern, s)
    if m == None:
        print(s)
        return None
    replace_pattern = lambda date: str(2018+int(date.group('r'))) + '-' + date.group('m') + '-' + date.group('d') + ' ' + date.group('H') + ':00:00'
    en_datetime = re.sub(find_pattern, replace_pattern, s)
    tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
    en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    return en_datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

writedata = {}
writedata['lastupdate'] = ''
writedata['summary'] = {'infectionTotal': 0, 'release': 0}
writedata['total'] = []
writedata['today'] = []

# ファイルのダウンロード
'''
domain = 'https://www.pref.okinawa.lg.jp'
#url = domain + '/site/hoken/chiikihoken/kekkaku/covid19_hasseijoukyou.html'
url = domain + '/site/hoken/kansen/soumu/covid19_hasseijoukyou.html'
'''
domain = 'https://www.pref.okinawa.lg.jp'
url = domain + '/site/hoken/kansen/soumu/press/20200214_covid19_pr1.html'

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find(id="tmp_contents").find_all('a')

foundFilePDF = False
foundFilePNG = False

#'20220813kichiichiran'

for link in links:
    href = link.get('href')
    if href and 'pdf' in href and ('kichi' in href or 'kiti' in href):
        file_name = href.split("/")[-1]
        file_href = href
        foundFilePDF = True
        print(file_name)

if foundFilePDF is False:
    for link in links:
        href = link.get('href')
        if href and 'png' in href and ('kichi' in href or 'kiti' in href):
            file_name = href.split("/")[-1]
            file_href = href
            foundFilePNG = True
            print(file_name)

if foundFilePDF is True:
    download_url = domain + file_href
    urllib.request.urlretrieve(download_url, './pdf/' + file_name)
    print("PDF downloaded at: pdf/" + file_name)
    resize_pdf_us.resize('./pdf/'+file_name, './pdf/resize_us.pdf')
    dummy_line_us.output_dummy('./component/dummy_line_us.pdf')
    dummy_line_us.output_mergePDF('./component/dummy_line_us.pdf', './pdf/resize_us.pdf', './pdf/processed_latest_us.pdf')
    pdf = pdfplumber.open('./pdf/processed_latest_us.pdf')

    for page in pdf.pages:

        bounding_box = (310, 60, 480, 90)
        page_crop = page.within_bbox(bounding_box)
        page_crop.to_image(resolution=200).save("./snapshot/lastupdate_us.png", format="PNG")
        writedata['lastupdate'] = convertKanjiDateTime2En(page_crop.extract_text())

        if writedata['lastupdate'] != None:

            tables = page.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "intersection_y_tolerance": 1,
                "min_words_horizontal": 2,
            })

            for table in tables:
                localDf = pd.DataFrame(table, columns=["場所", "昨日まで", "新規陽性者", "合計"])
                print(localDf)
                for index, row in localDf.iterrows():
                    if row['場所'] == None:
                        print('none')
                    elif len(row['場所']) == 0:
                        print('empty')
                    elif row['場所'] == '所属':
                        break
                    elif row['場所'].find('隔離解除') != -1:
                        writedata['summary']['release'] = int(row['合計'])
                    elif row['場所'] == '合計':
                        writedata['summary']['infectionTotal'] = int(row['合計'])
                    elif row['場所'] != '場所':
                        if row['合計'] == '':
                            writedata['total'].append({'name': row['場所'],'cases': 0})
                        else:
                            writedata['total'].append({'name': row['場所'],'cases': int(row['合計'])})
                        if row['新規陽性者'] == '':
                            writedata['today'].append({'name': row['場所'],'cases': 0})
                        else:
                            writedata['today'].append({'name': row['場所'],'cases': int(row['新規陽性者'])})

elif foundFilePNG is True:
    download_url = domain + file_href
    urllib.request.urlretrieve(download_url, './pdf/' + file_name)
    print("PNG downloaded at: pdf/" + file_name)

print(writedata)
if writedata['lastupdate'] != None:
    # 情報の保存
    update_wfile = open('./data/summary-military-us.json', 'w', encoding='utf8')
    json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
    update_wfile.close()
else:
    print('lastupdate is none.')
