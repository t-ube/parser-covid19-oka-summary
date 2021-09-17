import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import os
import json
import shutil
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

writedata = {}
writedata['hospitalize'] = 0
writedata['home'] = 0
writedata['hotel'] = 0
writedata['patient'] = 0
writedata['release'] = 0
writedata['total'] = 0
writedata['lastupdate'] = ''

def convertKanjiDateTime2En(kanji_datetime):
    find_pattern = r"^更新日：(?P<y>\d*)年(?P<m>\d*)月(?P<d>\d*)日"
    replace_pattern = lambda date: date.group('y') + '-' + date.group('m') + '-' + date.group('d') + ' ' + '00:00:00'
    en_datetime = re.sub(find_pattern, replace_pattern, kanji_datetime)
    tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
    en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    return en_datetime

def convertNinzuu(ninzuu):
    ninzuu = ninzuu.replace('\n','')
    ninzuu = ninzuu.replace('\r','')
    ninzuu = ninzuu.replace(u'\xa0', u'')
    ninzuu = ninzuu.replace(' ','')
    find_pattern = r"^(?P<n>\d*).*"
    replace_pattern = lambda count: count.group('n')
    counts = re.sub(find_pattern, replace_pattern, ninzuu)
    return int(counts)

def Download():
    domain = 'https://www.pref.okinawa.jp'
    url = domain + '/site/somu/yaeyama/shinko/020429_jyoukyou.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    update = soup.select_one("#tmp_update")
    writedata['lastupdate'] = convertKanjiDateTime2En(update.get_text())

    trList = soup.find_all("tr")
    for tr in trList:
        td = tr.find_all("td")
        if td[0] != None and td[1] != None:
            title = td[0].get_text()
            value = td[1].get_text()
            if '入院中' in title:
                writedata['hospitalize'] = convertNinzuu(value)
            elif '調整中' in title:
                writedata['home'] = convertNinzuu(value)
            elif '宿泊' in title:
                writedata['hotel'] = convertNinzuu(value)
            elif '解除' in title:
                writedata['release'] = convertNinzuu(value)
            elif '合計' in title:
                writedata['total'] = convertNinzuu(value)

    return


Download()

writedata['patient'] = writedata['hospitalize'] + writedata['home'] + writedata['hotel']
print(writedata)

# 情報の保存
update_wfile = open('./data/summary-isg.json', 'w', encoding='utf8')
json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
update_wfile.close()
