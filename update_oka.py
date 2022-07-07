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
    if kanji_datetime == None:
        return None
    find_pattern = r"^(?P<m>\d*)月(?P<d>\d*)日.*"
    m = re.match(find_pattern, kanji_datetime)
    if m != None:
        def replace_pattern(date): return str(
            2021) + '-' + date.group('m') + '-' + date.group('d') + ' ' + '12:00:00'
        en_datetime = re.sub(find_pattern, replace_pattern, kanji_datetime)
        tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
        en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        return en_datetime
    return None

def getNumber(text):
    if text == None:
        return None
    text = text.replace(',', '')
    find_pattern = r"^(?P<number>\d*).*"
    m = re.match(find_pattern, text)
    if m != None:
        def replace_pattern(conv): return str(conv.group('number'))
        convText = re.sub(find_pattern, replace_pattern, text)
        return int(convText)
    return None

def convertKanjiDateTime2EnV2(kanji_datetime):
    if kanji_datetime == None:
        return None
    find_pattern = r"^R(?P<reiwa>\d*).(?P<m>\d*).(?P<d>\d*).*"
    m = re.match(find_pattern, kanji_datetime)
    if m != None:
        def replace_pattern(date): return str(int(date.group('reiwa'))+2018
            ) + '-' + date.group('m') + '-' + date.group('d') + ' ' + '12:00:00'
        en_datetime = re.sub(find_pattern, replace_pattern, kanji_datetime)
        tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
        en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        return en_datetime
    return None

def convertKanjiDateTime2EnV3(kanji_datetime):
    if kanji_datetime == None:
        return None
    find_pattern = r"^令和(?P<reiwa>\d*)年(?P<m>\d*)月(?P<d>\d*)日.*"
    m = re.match(find_pattern, kanji_datetime)
    if m != None:
        def replace_pattern(date): return str(int(date.group('reiwa'))+2018
            ) + '-' + date.group('m') + '-' + date.group('d') + ' ' + '12:00:00'
        en_datetime = re.sub(find_pattern, replace_pattern, kanji_datetime)
        tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
        en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        return en_datetime
    return None

def get_pdf_typeA(file):
    resize_pdf_oka.resize(file, './pdf/resize_oka.pdf')
    dummy_line_oka.output_dummy_TypeA('./component/dummy_line_oka.pdf')
    dummy_line_oka.output_mergePDF('./component/dummy_line_oka.pdf',
                                './pdf/resize_oka.pdf', './pdf/processed_latest_oka.pdf')
    pdf = pdfplumber.open('./pdf/processed_latest_oka.pdf')
    return pdf

def get_pdf_typeB(file):
    resize_pdf_oka.resize(file, './pdf/resize_oka.pdf')
    dummy_line_oka.output_dummy_TypeB('./component/dummy_line_oka.pdf')
    dummy_line_oka.output_mergePDF('./component/dummy_line_oka.pdf',
                                './pdf/resize_oka.pdf', './pdf/processed_latest_oka.pdf')
    pdf = pdfplumber.open('./pdf/processed_latest_oka.pdf')
    return pdf

def get_pdf_typeC(file):
    resize_pdf_oka.resize(file, './pdf/resize_oka.pdf')
    dummy_line_oka.output_dummy_TypeC('./component/dummy_line_oka.pdf')
    dummy_line_oka.output_mergePDF('./component/dummy_line_oka.pdf',
                                './pdf/resize_oka.pdf', './pdf/processed_latest_oka.pdf')
    pdf = pdfplumber.open('./pdf/processed_latest_oka.pdf')
    return pdf

def get_pdf_typeD(file):
    resize_pdf_oka.resize(file, './pdf/resize_oka.pdf')
    dummy_line_oka.output_dummy_TypeD('./component/dummy_line_oka.pdf')
    dummy_line_oka.output_mergePDF('./component/dummy_line_oka.pdf',
                                './pdf/resize_oka.pdf', './pdf/processed_latest_oka.pdf')
    pdf = pdfplumber.open('./pdf/processed_latest_oka.pdf')
    return pdf

def get_pdf_typeE(file):
    resize_pdf_oka.resize(file, './pdf/resize_oka.pdf')
    dummy_line_oka.output_dummy_TypeE('./component/dummy_line_oka.pdf')
    dummy_line_oka.output_mergePDF('./component/dummy_line_oka.pdf',
                                './pdf/resize_oka.pdf', './pdf/processed_latest_oka.pdf')
    pdf = pdfplumber.open('./pdf/processed_latest_oka.pdf')
    return pdf

def get_pdf_typeF(file):
    pdf = pdfplumber.open(file)
    return pdf

def pdf_to_data(pdf):
    for page in pdf.pages:
        bounding_box = (250, 74, 400, 90)
        page_crop = page.within_bbox(bounding_box)
        page_crop.to_image(resolution=200).save(
            "./snapshot/lastupdate_oka.png", format="PNG")
        writedata['lastupdate'] = convertKanjiDateTime2En(page_crop.extract_text())
        if writedata['lastupdate'] == None:
            return writedata
        tables = page.extract_tables({
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "intersection_y_tolerance": 1,
            "min_words_horizontal": 2,
        })
        for table in tables:
            localDf = pd.DataFrame(table)
            print(localDf)
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
                        if row[pos+3] == None:
                            return writedata
                        writedata['moderate'] = int(row[pos+3])
                elif row[pos].find('入院中') != -1:
                    if row[pos+1] == '' or row[pos+3] == '':
                        return writedata
                    writedata['hospitalize'] = int(row[pos+1])
                    writedata['severe'] = int(row[pos+3])
                elif row[pos].find('調整中') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['wait'] = int(row[pos+1])
                elif row[pos].find('宿泊') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['hotel'] = int(row[pos+1])
                elif row[pos].find('自宅') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['home'] = int(row[pos+1])
                elif row[pos].find('解除確認') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['checkout'] = int(row[pos+1])
                elif row[pos].find('勧告解除') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['release'] = int(row[pos+1])
                elif row[pos].find('死亡') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['dead'] = int(row[pos+1])
    writedata['patient'] = writedata['hospitalize'] + writedata['wait'] + \
        writedata['hotel'] + writedata['home'] + writedata['checkout']
    return writedata

def pdf_to_dataV2(pdf):
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
            print(localDf)
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
                        if row[pos+3] == None:
                            return writedata
                        writedata['moderate'] = int(row[pos+3])
                elif row[pos].find('入院中') != -1:
                    if row[pos+1] == '' or row[pos+3] == '':
                        return writedata
                    writedata['hospitalize'] = int(row[pos+1])
                    writedata['severe'] = int(row[pos+3])
                elif row[pos].find('調整中') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['wait'] = int(row[pos+1])
                elif row[pos].find('宿泊') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['hotel'] = int(row[pos+1])
                elif row[pos].find('自宅') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['home'] = int(row[pos+1])
                elif row[pos].find('解除確認') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['checkout'] = int(row[pos+1])
                elif row[pos].find('勧告解除') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['release'] = int(row[pos+1])
                elif row[pos].find('死亡') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['dead'] = int(row[pos+1])
                elif row[pos].find('実数') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['patient'] = int(row[pos+1])
    return writedata

def pdf_to_dataV3(pdf):
    for page in pdf.pages:
        bounding_box = (410, 74, 550, 90)
        page_crop = page.within_bbox(bounding_box)
        page_crop.to_image(resolution=200).save(
            "./snapshot/lastupdate_oka.png", format="PNG")
        writedata['lastupdate'] = convertKanjiDateTime2EnV2(page_crop.extract_text())
        tables = page.extract_tables({
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "intersection_y_tolerance": 1,
            "min_words_horizontal": 2,
        })
        for table in tables:
            localDf = pd.DataFrame(table)
            print(localDf)
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
                        if row[pos+3] == None:
                            return writedata
                        writedata['moderate'] = int(row[pos+3])
                elif row[pos].find('入院中') != -1:
                    if row[pos+1] == '' or row[pos+3] == '':
                        return writedata
                    writedata['hospitalize'] = int(row[pos+1])
                    writedata['severe'] = int(row[pos+3])
                elif row[pos].find('調整中') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['wait'] = int(row[pos+1])
                elif row[pos].find('宿泊') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['hotel'] = int(row[pos+1])
                elif row[pos].find('自宅') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['home'] = int(row[pos+1])
                elif row[pos].find('解除確認') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['checkout'] = int(row[pos+1])
                elif row[pos].find('勧告解除') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['release'] = int(row[pos+1])
                elif row[pos].find('死亡') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['dead'] = int(row[pos+1])
                elif row[pos].find('実数') != -1:
                    if row[pos+1] == '':
                        return writedata
                    writedata['patient'] = getNumber(row[pos+1])
    return writedata

def pdf_to_dataV4(pdf):
    page = pdf.pages[0]
    bounding_box = (680, 58, 810, 74)
    page_crop = page.within_bbox(bounding_box)
    page_crop.to_image(resolution=200).save(
        "./snapshot/lastupdate_oka.png", format="PNG")
    writedata['lastupdate'] = convertKanjiDateTime2EnV3(page_crop.extract_text())
    tables = page.extract_tables({
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "intersection_y_tolerance": 1,
        "min_words_horizontal": 2,
    })
    for table in tables:
        localDf = pd.DataFrame(table)
        print(localDf)
        pos = -1
        for index, row in localDf.iterrows():
            if row[11] != None and row[11].find('累計療養者数') != -1:
                pos = 0
                break
        if pos == -1:
            continue
        for index, row in localDf.iterrows():
            if index == 3:
                print(row)
                writedata['hospitalize'] = getNumber(row[2])
                writedata['severe'] = getNumber(row[3])
                writedata['moderate'] = getNumber(row[4])
                writedata['wait'] = getNumber(row[5])
                writedata['hotel'] = getNumber(row[6])
                writedata['home'] = getNumber(row[7])
                writedata['checkout'] = getNumber(row[8])
                writedata['dead'] = getNumber(row[9])
                writedata['release'] = getNumber(row[10])
                writedata['patient'] = getNumber(row[11])
    return writedata

def pdf_to_dataV5(pdf):
    page = pdf.pages[0]
    bounding_box = (640, 54, 810, 74)
    page_crop = page.within_bbox(bounding_box)
    page_crop.to_image(resolution=200).save(
        "./snapshot/lastupdate_oka.png", format="PNG")
    writedata['lastupdate'] = convertKanjiDateTime2EnV3(page_crop.extract_text())
    tables = page.extract_tables({
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "intersection_y_tolerance": 1,
        "min_words_horizontal": 2,
    })
    for table in tables:
        localDf = pd.DataFrame(table)
        print(localDf)
        pos = -1
        for index, row in localDf.iterrows():
            if row[1] != None and row[1].find('累計療養者数') != -1:
                pos = 0
                break
        if pos == -1:
            continue
        for index, row in localDf.iterrows():
            if index == 3:
                print(row)
                writedata['patient'] = getNumber(row[1])
                writedata['hospitalize'] = getNumber(row[3])
                writedata['severe'] = getNumber(row[4])
                writedata['moderate'] = getNumber(row[5])
                writedata['wait'] = getNumber(row[6])
                writedata['hotel'] = getNumber(row[7])
                writedata['home'] = getNumber(row[8])
                writedata['checkout'] = getNumber(row[9])
                writedata['release'] = getNumber(row[10])
                writedata['dead'] = getNumber(row[11])
    return writedata

# ファイルのダウンロード
def downloadFile():
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

    if os.path.isfile(save_file):
        print("PDF downloaded skip: csv/" + file_name)
    else:
        urllib.request.urlretrieve(download_url, save_file)
        print("PDF downloaded at: csv/" + file_name)

    return save_file

save_file = downloadFile()

writedata = pdf_to_dataV5(get_pdf_typeF(save_file))
print(writedata)

'''
writedata = pdf_to_data(get_pdf_typeA(save_file))
print(writedata)
if writedata['release'] == 0:
    writedata = pdf_to_data(get_pdf_typeB(save_file))
print(writedata)
if writedata['release'] == 0:
    writedata = pdf_to_data(get_pdf_typeC(save_file))
print(writedata)
if writedata['release'] == 0:
    writedata = pdf_to_dataV2(get_pdf_typeD(save_file))
if writedata['release'] == 0:
    writedata = pdf_to_dataV3(get_pdf_typeE(save_file))
'''

# 情報の保存
update_wfile = open('./data/summary-oka.json', 'w', encoding='utf8')
json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
update_wfile.close()
