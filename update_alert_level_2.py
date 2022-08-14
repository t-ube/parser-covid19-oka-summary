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
import unicodedata

import resize_pdf_alert_level
import dummy_line_alert_level_2


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

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if os.path.exists('./data/alert-indicators-2.json') == False:
    print('Not found: data/alert-indicators-2.json')
    sys.exit(1)

update_rfile = open('./data/alert-indicators-2.json', 'r')
writedata = json.load(update_rfile)
update_rfile.close()

lastupdate = writedata['lastupdate']

def convertKanjiDateTime2En(kanji_datetime):
    s = unicodedata.normalize("NFKC", kanji_datetime)
    s = s.replace('\n', '')
    print(s)
    find_pattern = r"^令和(?P<y>\d*)年(?P<m>\d*)月(?P<d>\d*)日(?P<H>\d*)時時点"
    replace_pattern = lambda date: str(2022) + '-' + date.group('m') + '-' + date.group('d') + ' ' + date.group('H') + ':00:00'
    en_datetime = re.sub(find_pattern, replace_pattern, s)
    tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
    en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    return en_datetime

def convertDateTimeText2DateText(datetimeText):
    tdatetime = datetime.datetime.strptime(datetimeText, '%Y-%m-%d %H:%M:%S')
    return tdatetime.strftime('%Y/%m/%d')

def getTypeA(localDf):
    print('getTypeA')
    datamapping = False
    for index, row in localDf.iterrows():
        if index == 0  and str(row[3]).find('時点') != -1:
            writedata['lastupdate'] = convertKanjiDateTime2En(str(row[3]))
            print(writedata['lastupdate'])
            writedata['alertIndicators']['date'].append(convertDateTimeText2DateText(writedata['lastupdate']))
            datamapping = True
        elif index == 1 and str(row[2]).find('新規陽性者数') != -1:
            print(row[3])
            writedata['alertIndicators']['patients'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 2 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            writedata['alertIndicators']['bed_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 3 and str(row[2]).find('重症') != -1 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            writedata['alertIndicators']['severe_bed_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 4 and str(row[2]).find('重症') != -1 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            writedata['alertIndicators']['severe_bed_rate_ken'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 5 and str(row[2]).find('療養者数') != -1:
            print(row[3])
            writedata['alertIndicators']['recuperation'].append(int(re.sub("\\D", "", row[3])))
        elif index == 6 and str(row[2]).find('経路不明') != -1:
            print(row[3])
            writedata['alertIndicators']['unknown_route_rate7days'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 7 and str(row[2]).find('陽性率') != -1:
            print(row[3])
            writedata['alertIndicators']['positive_rate7days'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 8 and str(row[2]).find('入院率') != -1:
            print(row[3])
            writedata['alertIndicators']['hospitalized_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 9 and str(row[2]).find('前週比') != -1:
            print(row[3])
            writedata['alertIndicators']['lastweek_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 10 and str(row[2]).find('予測ツール') != -1:
            print(row[3])
            if row[3] == '―':
                writedata['alertIndicators']['predict_tool'].append(None)
            else:
                writedata['alertIndicators']['predict_tool'].append(int(re.sub("\\D", "", row[3])))
    return datamapping

def checkNoneData(param):
    data = re.search(r'－', param)
    if data != None:
        return True
    dataList = re.findall("\d+\.\d+", param)
    if dataList != None:
        return False
    data = re.sub("\\D", "", param)
    if data != None:
        return False
    return True

def getTypeC(localDf):
    print('getTypeC')
    datamapping = False
    for index, row in localDf.iterrows():
        if index == 0  and (len(row) > 3) and str(row[3]).find('時点') != -1:
            writedata['lastupdate'] = convertKanjiDateTime2En(str(row[3]))
            print(writedata['lastupdate'])
            writedata['alertIndicators']['date'].append(convertDateTimeText2DateText(writedata['lastupdate']))
            datamapping = True
        elif index == 2 and (len(row) > 2) and str(row[2]).find('新規陽性者数') != -1:
            print(row[3])
            writedata['alertIndicators']['patients'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 3 and (len(row) > 2) and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            writedata['alertIndicators']['bed_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 4 and (len(row) > 2) and str(row[2]).find('重症') != -1 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            if (len(row) > 3) and checkNoneData(row[3]):
                writedata['alertIndicators']['severe_bed_rate'].append(None)
            else:
                writedata['alertIndicators']['severe_bed_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 6 and (len(row) > 2) and str(row[2]).find('重症') != -1 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['severe_bed_rate_ken'].append(None)
            else:
                writedata['alertIndicators']['severe_bed_rate_ken'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 8 and (len(row) > 2) and str(row[2]).find('療養者数') != -1:
            print(row[3])
            if (len(row) > 3) and checkNoneData(row[3]):
                writedata['alertIndicators']['recuperation'].append(None)
            else:
                writedata['alertIndicators']['recuperation'].append(int(re.sub("\\D", "", row[3])))
        elif index == 10 and (len(row) > 2) and str(row[2]).find('経路不明') != -1:
            print(row[3])
            if (len(row) > 3) and checkNoneData(row[3]):
                writedata['alertIndicators']['unknown_route_rate7days'].append(None)
            else:
                writedata['alertIndicators']['unknown_route_rate7days'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 12 and str(row[2]).find('陽性率') != -1:
            print(row[3])
            if (len(row) > 3) and checkNoneData(row[3]):
                writedata['alertIndicators']['positive_rate7days'].append(None)
            else:
                writedata['alertIndicators']['positive_rate7days'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 14 and str(row[2]).find('入院率') != -1:
            print(row[3])
            if (len(row) > 3) and checkNoneData(row[3]):
                writedata['alertIndicators']['hospitalized_rate'].append(None)
            else:
                writedata['alertIndicators']['hospitalized_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 16 and str(row[2]).find('前週比') != -1:
            print(row[3])
            if (len(row) > 3) and checkNoneData(row[3]):
                writedata['alertIndicators']['lastweek_rate'].append(None)
            else:
                writedata['alertIndicators']['lastweek_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 18 and str(row[2]).find('予測ツール') != -1:
            print(row[3])
            if (len(row) > 3) and checkNoneData(row[3]):
                writedata['alertIndicators']['predict_tool'].append(None)
            else:
                writedata['alertIndicators']['predict_tool'].append(int(re.sub("\\D", "", row[3])))
    return datamapping

def getTypeB(localDf):
    print('getTypeB')
    datamapping = False
    for index, row in localDf.iterrows():
        if index == 0  and str(row[3]).find('時点') != -1:
            writedata['lastupdate'] = convertKanjiDateTime2En(str(row[3]))
            print(writedata['lastupdate'])
            writedata['alertIndicators']['date'].append(convertDateTimeText2DateText(writedata['lastupdate']))
            datamapping = True
        elif index == 2 and str(row[2]).find('新規陽性者数') != -1:
            print(row[3])
            writedata['alertIndicators']['patients'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 3 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            writedata['alertIndicators']['bed_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 4 and str(row[2]).find('重症') != -1 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['severe_bed_rate'].append(None)
            else:
                writedata['alertIndicators']['severe_bed_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 6 and str(row[2]).find('重症') != -1 and str(row[2]).find('病床使用率') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['severe_bed_rate_ken'].append(None)
            else:
                writedata['alertIndicators']['severe_bed_rate_ken'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 8 and str(row[2]).find('療養者数') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['recuperation'].append(None)
            else:
                writedata['alertIndicators']['recuperation'].append(int(re.sub("\\D", "", row[3])))
        elif index == 10 and str(row[2]).find('経路不明') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['unknown_route_rate7days'].append(None)
            else:
                writedata['alertIndicators']['unknown_route_rate7days'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 12 and str(row[2]).find('陽性率') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['positive_rate7days'].append(None)
            else:
                writedata['alertIndicators']['positive_rate7days'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 14 and str(row[2]).find('入院率') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['hospitalized_rate'].append(None)
            else:
                writedata['alertIndicators']['hospitalized_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 16 and str(row[2]).find('前週比') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['lastweek_rate'].append(None)
            else:
                writedata['alertIndicators']['lastweek_rate'].append(float(re.findall("\d+\.\d+", row[3])[0]))
        elif index == 18 and str(row[2]).find('予測ツール') != -1:
            print(row[3])
            if checkNoneData(row[3]):
                writedata['alertIndicators']['predict_tool'].append(None)
            else:
                writedata['alertIndicators']['predict_tool'].append(int(re.sub("\\D", "", row[3])))
    return datamapping

# ファイルのダウンロード
domain = 'https://www.pref.okinawa.lg.jp'
url = domain + '/site/chijiko/koho/corona/20200702.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find(id="tmp_contents").find_all('a')

for link in links:
    href = link.get('href')
    if href and 'pdf' in href:
        file_name = href.split("/")[-1]
        print('Find pdf:'+file_name)
        if 'bun' in file_name:
            print('Find bun')
        elif 'handan' in file_name:
            print('Find handan')
        elif 'keikaireberu' in file_name:
            print('Find keikaireberu')
            file_href = href
            find_file = file_name
            print('OK:'+find_file)
            break

download_url = domain + file_href
urllib.request.urlretrieve(download_url, './pdf/' + find_file)
print("PDF downloaded at: pdf/" + find_file)

#resize_pdf.resize('./pdf/'+find_file, './pdf/resize.pdf')
rename_src = datetime.datetime.today().strftime('keikaireberu_%Y-%m-%d.pdf')
copyFile('./pdf/'+find_file,'./archive/'+rename_src)

print('./pdf/'+find_file)

dummy_line_alert_level_2.output_dummy('./component/dummy_line_alert_level.pdf')
dummy_line_alert_level_2.output_mergePDF('./component/dummy_line_alert_level.pdf', './pdf/'+find_file, './pdf/processed_latest_alert_level.pdf')

pdf = pdfplumber.open('./pdf/processed_latest_alert_level.pdf')

datamapping = False

for page in pdf.pages:

    tables = page.extract_tables({
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "intersection_y_tolerance": 1,
        "min_words_horizontal": 2,
    })

    #print(tables)

    for table in tables:
        localDf = pd.DataFrame(table)
        print(localDf)
        if len(localDf) > 10:
            datamapping = getTypeC(localDf)
            break
        else:
            datamapping = getTypeA(localDf)
            break

if datamapping == False:
    print('failed to mapping')
    sys.exit(0)#sys.exit(1)
elif datetime.datetime.strptime(lastupdate, '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(writedata['lastupdate'], '%Y-%m-%d %H:%M:%S'):
    # 更新情報の保存
    update_wfile = open('./data/alert-indicators-2.json', 'w', encoding='utf8')
    json.dump(writedata, update_wfile, ensure_ascii=False)
    update_wfile.close()
    sys.exit(0)
else:
    print('skip update')
    print(lastupdate)
    print(writedata['lastupdate'])
    sys.exit(0)
