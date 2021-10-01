import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import os
import json
import unicodedata

os.chdir(os.path.dirname(os.path.abspath(__file__)))

writedata = {}
writedata['hospitalize'] = 0
writedata['home'] = 0
writedata['hotel'] = 0
writedata['institution'] = 0
writedata['patient'] = 0
writedata['release'] = 0
writedata['total'] = 0
writedata['lastupdate'] = ''

def convertKanjiDateTime2En(kanji_datetime):
    s = unicodedata.normalize("NFKC", kanji_datetime)
    s = s.replace('\n', '')
    find_pattern = r".*令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日.*"

    replace_reiwa = lambda date: date.group('r')
    reiwa = re.sub(find_pattern, replace_reiwa, s)
    year = str(int(reiwa,10) + 2018)

    replace_pattern = lambda date: year + '-' + date.group('m') + '-' + date.group('d') + ' ' + '00:00:00'
    en_datetime = re.sub(find_pattern, replace_pattern, s)
    tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')

    en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    return en_datetime

def convertNinzuu(ninzuu):
    ninzuu = ninzuu.replace('\n','')
    ninzuu = ninzuu.replace('\r','')
    ninzuu = ninzuu.replace(',','')
    ninzuu = ninzuu.replace(u'\xa0', u'')
    ninzuu = ninzuu.replace(' ','')
    find_pattern = r"^(?P<n>\d*)人"
    replace_pattern = lambda count: count.group('n')
    counts = re.sub(find_pattern, replace_pattern, ninzuu)
    return int(counts)

def Download():
    domain = 'https://www.city.miyakojima.lg.jp'
    url = domain + '/kurashi/kenkou/2020-0306-1115-78.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    strongList = soup.select("strong")
    for strong in strongList:
        txt = strong.get_text()
        if '宮古島市内の患者発生状況' in txt:
            writedata['lastupdate'] = convertKanjiDateTime2En(txt)
            print(writedata['lastupdate'])

    trList = soup.find_all("tr")
    if trList != None and trList[1] != None:
        tdList = trList[1].find_all("td")
        if tdList != None:
            writedata['total'] = convertNinzuu((tdList[1].get_text()))
            writedata['hospitalize'] = convertNinzuu((tdList[2].get_text()))
            writedata['hotel'] = convertNinzuu((tdList[3].get_text()))
            writedata['home'] = convertNinzuu((tdList[4].get_text()))
            writedata['institution'] = convertNinzuu((tdList[5].get_text()))
            writedata['wait'] = convertNinzuu((tdList[6].get_text()))
            writedata['release'] = convertNinzuu((tdList[7].get_text()))
            writedata['dead'] = convertNinzuu((tdList[8].get_text()))
    return

Download()

writedata['patient'] = writedata['hospitalize'] + writedata['home'] + writedata['hotel'] + writedata['institution'] + writedata['wait']
print(writedata)

# 情報の保存
update_wfile = open('./data/summary-mmy.json', 'w', encoding='utf8')
json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
update_wfile.close()
