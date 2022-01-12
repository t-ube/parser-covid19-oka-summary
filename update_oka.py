import requests
import urllib.request

from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
import datetime
import os
import pathlib
import json
import sys
import pdfplumber
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader

import time

import dummy_line_oka
import resize_pdf_oka

os.chdir(os.path.dirname(os.path.abspath(__file__)))

writedata = {}
writedata['hospitalize'] = 0
writedata['wait'] = 0
writedata['hotel'] = 0
writedata['home'] = 0
writedata['checkout'] = 0
writedata['release'] = 0
writedata['dead'] = 0
writedata['patient'] = 0
writedata['severe'] = 0
writedata['moderate'] = 0
writedata['lastupdate'] = ''


def convertKanjiDateTime2En(kanji_datetime):
    find_pattern = r"^(?P<m>\d*)月(?P<d>\d*)日.*"

    def replace_pattern(date): return str(
        2021) + '-' + date.group('m') + '-' + date.group('d') + ' ' + '12:00:00'
    en_datetime = re.sub(find_pattern, replace_pattern, kanji_datetime)
    tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
    en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    return en_datetime


# ファイルのダウンロード
domain = 'https://www.pref.okinawa.lg.jp'
url = domain + '/site/hoken/kansen/soumu/press/20200214_covid19_pr1.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find(id="tmp_contents").find_all('a')

for link in links:
    href = link.get('href')
    if href and 'pdf' in href:
        file_name = href.split("/")[-1]
        print('Find pdf:'+file_name)
        if 'hou' in file_name:
            print('Find hou')
            file_href = href
            find_file = file_name
            print('OK:'+find_file)
            break

download_url = domain + file_href
save_file = './pdf/' + find_file

urllib.request.urlretrieve(download_url, save_file)
print("PDF downloaded at: pdf/" + find_file)

resize_pdf_oka.resize(save_file, './pdf/resize_oka.pdf')
dummy_line_oka.output_dummy_TypeB('./component/dummy_line_oka.pdf')
dummy_line_oka.output_mergePDF('./component/dummy_line_oka.pdf',
                               './pdf/resize_oka.pdf', './pdf/processed_latest_oka.pdf')

pdf = pdfplumber.open('./pdf/processed_latest_oka.pdf')

for page in pdf.pages:

    bounding_box = (250, 74, 400, 90)
    page_crop = page.within_bbox(bounding_box)
    page_crop.to_image(resolution=200).save(
        "./snapshot/lastupdate_oka.png", format="PNG")
    writedata['lastupdate'] = convertKanjiDateTime2En(page_crop.extract_text())

    tables = page.extract_tables({
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "intersection_y_tolerance": 1,
        "min_words_horizontal": 2,
    })

    for table in tables:
        localDf = pd.DataFrame(table)

        pos = -1
        for index, row in localDf.iterrows():
            if row[0] != None and row[0].find('入院中') != -1:
                pos = 0
                break
            elif row[1] != None and row[1].find('入院中') != -1:
                pos = 1
                break

        if pos == -1:
            break
        
        for index, row in localDf.iterrows():
            if row[pos] == None:
                print('none')
            elif len(row[pos]) == 0:
                if (index == 2 or index == 3) and row[pos+2] != None and row[pos+2].find('中等') != -1:
                    writedata['moderate'] = int(row[pos+3])
            elif row[pos].find('入院中') != -1:
                writedata['hospitalize'] = int(row[pos+1])
                writedata['severe'] = int(row[pos+3])
            elif row[pos].find('調整中') != -1:
                writedata['wait'] = int(row[pos+1])
            elif row[pos].find('宿泊') != -1:
                writedata['hotel'] = int(row[pos+1])
            elif row[pos].find('自宅') != -1:
                writedata['home'] = int(row[pos+1])
            elif row[pos].find('解除確認') != -1:
                writedata['checkout'] = int(row[pos+1])
            elif row[pos].find('勧告解除') != -1:
                writedata['release'] = int(row[pos+1])
            elif row[pos].find('死亡') != -1:
                writedata['dead'] = int(row[pos+1])

writedata['patient'] = writedata['hospitalize'] + writedata['wait'] + \
    writedata['hotel'] + writedata['home'] + writedata['checkout']

print(writedata)

# 情報の保存
update_wfile = open('./data/summary-oka.json', 'w', encoding='utf8')
json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
update_wfile.close()
