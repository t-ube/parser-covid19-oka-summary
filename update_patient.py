import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import os
import json
import time
import csv
import downlod_patient


os.chdir(os.path.dirname(os.path.abspath(__file__)))

def convertKanjiDateTime2En(kanji_datetime):
    s = kanji_datetime.replace('\n', '')

    print(s)
    find_pattern = r"^更新日：(?P<y>\d*)年(?P<m>\d*)月(?P<d>\d*)日.*"

    m = re.match(find_pattern, s)
    if m == None:
        return None

    replace_pattern = lambda date: date.group(
        'y') + '-' + date.group('m') + '-' + date.group('d') + ' ' + '00:00:00'
    en_datetime = re.sub(find_pattern, replace_pattern, s)
    tdatetime = datetime.datetime.strptime(en_datetime, '%Y-%m-%d %H:%M:%S')
    en_datetime = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    return en_datetime

def convertTitle2DateTime(title):
    s = title.replace('\n', '')
    s = s.replace(')', '）')
    s = s.replace('(', '（')
    s = s.replace(' ', '')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_reiwa = lambda date: date.group('r')
        reiwa = re.sub(find_pattern, replace_reiwa, s)
        year = str(int(reiwa, 10) + 2018)

        replace_pattern = lambda date: year + '-' + \
            date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)例目-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_reiwa = lambda date: date.group('r')
        reiwa = re.sub(find_pattern, replace_reiwa, s)
        year = str(int(reiwa, 10) + 2018)

        replace_pattern = lambda date: year + '-' + \
            date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)-(?P<e>\d*)目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_reiwa = lambda date: date.group('r')
        reiwa = re.sub(find_pattern, replace_reiwa, s)
        year = str(int(reiwa, 10) + 2018)

        replace_pattern = lambda date: year + '-' + \
            date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_reiwa = lambda date: date.group('r')
        reiwa = re.sub(find_pattern, replace_reiwa, s)
        year = str(int(reiwa, 10) + 2018)

        replace_pattern = lambda date: year + '-' + \
            date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)例目・(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        return '2020-xx-xx'

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        return '2020-xx-xx'

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*例目)-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        return '2020-xx-xx'

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)～(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        return '2020-xx-xx'

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        return '2020-xx-xx'

    return None

def convertReiwa2Year(date):
    find_pattern = r".*令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日.*"
    m = re.match(find_pattern, date)
    if m != None:
        replace_reiwa = lambda date: date.group('r')
        reiwa = re.sub(find_pattern, replace_reiwa, date)
        year = str(int(reiwa, 10) + 2018)

        replace_pattern = lambda date: year + '-' + \
            date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, date)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')
    return date

def convertTitle2DateTimeV2(title):
    s = title.replace('\n', '')
    s = s.replace(')', '）')
    s = s.replace('(', '（')
    s = s.replace(' ', '')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<sp>\s*)(?P<d>\d*)日（~(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_reiwa = lambda date: date.group('r')
        reiwa = re.sub(find_pattern, replace_reiwa, s)
        year = str(int(reiwa, 10) + 2018)

        replace_pattern = lambda date: year + '-' + \
            date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    return None

def convertTitle2EndCaseV2(title):
    s = title.replace('\n', '')
    s = s.replace(')', '）')
    s = s.replace('(', '（')
    s = s.replace(' ', '')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<sp>\s*)(?P<d>\d*)日（~(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    return None

def convertCase498930(case):
    if case == 498930:
        return 49930
    return case

def convertCase5014(case):
    if case == 5014:
        return 50214
    return case

def convertMissCase(case):
    return convertCase5014(convertCase498930(case))

def convertTitle2BeginCase(title):
    s = title.replace('\n', '')
    s = s.replace(')', '）')
    s = s.replace('(', '（')
    s = s.replace(' ', '')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)例目-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)-(?P<e>\d*)目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)例目・(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*例目)-(?P<e>\d*)例目）.*"
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)～(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    
    return None

def convertTitle2EndCase(title):
    s = title.replace('\n', '')
    s = s.replace(')', '）')
    s = s.replace('(', '（')
    s = s.replace(' ', '')

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)例目-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)-(?P<e>\d*)目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：令和(?P<r>\d*)年(?P<m>\d*)月(?P<d>\d*)日（県内(?P<b>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)例目・(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)-(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*例目)-(?P<e>\d*)例目）.*"
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)～(?P<e>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('e')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    find_pattern = r".*第(?P<n>\d*)報：（県内(?P<b>\d*)例目）.*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda case: case.group('b')
        case = re.sub(find_pattern, replace_pattern, s)
        return int(case)

    return None


def Download():
    # ファイルのダウンロード
    domain = 'https://www.pref.okinawa.lg.jp'
    #url = domain + '/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html'
    url = domain + '/site/hoken/kansen/soumu/press/20200214_covid19_pr1.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find(id="tmp_contents").find_all('a')

    for link in links:
        href = link.get('href')
        if href and ('youseisya' in href or 'youseisha' in href) and 'csv' in href:
            file_name = href.split("/")[-1]
            file_href = href
            print(file_name)
            break

    download_url = domain + file_href
    download_file = './csv/' + file_name
    if os.path.isfile(download_file):
        print("CSV downloaded skip: csv/" + file_name)
    else:
        urllib.request.urlretrieve(download_url, download_file)
        print("CSV downloaded at: csv/" + file_name)
    return download_file
    
def getOpenDate(savefile,resource):
    domain = 'https://www.pref.okinawa.lg.jp'
    # url = domain + '/site/hoken/kansen/soumu/press/20201019.html'
    url = domain + resource
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    update = soup.select_one("#tmp_update")

    df = pd.DataFrame(None,columns = ['opendate' , 'first_case', 'last_case'])

    h4List = soup.find_all("h4")
    for h4 in h4List:
        if h4 != None and h4 != None:
            title = h4.get_text()
            date = convertTitle2DateTime(title)
            if date != None:
                df = df.append({'opendate': date, 'first_case': convertMissCase(convertTitle2BeginCase(title)), 'last_case': convertTitle2EndCase(title)}, ignore_index=True)

    print(df)
    df.to_csv(savefile,encoding="'utf-8-sig",index = False)
    return

def getOpenDateV2(savefile,resource):
    domain = 'https://www.pref.okinawa.lg.jp'
    # url = domain + '/site/hoken/kansen/soumu/press/20201019.html'
    url = domain + resource
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    update = soup.select_one("#tmp_update")

    df = pd.DataFrame(None,columns = ['opendate' , 'first_case', 'last_case'])

    liList = soup.find_all("li")
    prev_case = 174925 #700報
    for li in reversed(liList):
        if li != None and li != None:
            title = li.get_text()
            date = convertTitle2DateTimeV2(title)
            if date != None:
                cur_case = convertTitle2EndCaseV2(title)
                df = df.append({'opendate': date, 'first_case': prev_case+1, 'last_case': cur_case}, ignore_index=True)
                prev_case = cur_case

    df = df.iloc[::-1]
    print(df)
    df.to_csv(savefile,encoding="'utf-8-sig",index = False)
    return

def eraseHeader(file_in,file_out) :
    df = pd.read_csv(filepath_or_buffer=file_in,
    encoding="ms932", sep=",")
    df.to_csv(file_out, encoding='utf_8_sig', header=False, index=False)

def rejectMissing(file_in,file_out) :
    df = pd.read_csv(filepath_or_buffer=file_in,
    encoding="utf_8_sig", sep=",", header=None,
    names=["caseNo","sex","age","onsetDate","fixDate","area","work","route"],
    dtype={'caseNo':str,'sex':str,'age':str,'onsetDate':str,'fixDate':str,'area':str,'work':str,'route':str},
    converters={"onsetDate":convertKanjiDate2EnDate, "fixDate":convertKanjiDate2EnDate}
    )
    df = df[(df['caseNo'] != '＊') & (df['age'] != '欠番') & (df['caseNo'] != '')]
    df['caseNo'] = df['caseNo'].astype('i8')
    df = df.sort_values('caseNo', ascending=True)
    df.to_csv(file_out, encoding='utf_8_sig', header=True, index=False)

def removeReturn(file_in,file_out):
    df = pd.read_csv(filepath_or_buffer=file_in,
    encoding="utf_8_sig", sep=",")
    df = df.replace('\n', '', regex=True)
    df.to_csv(file_out, encoding='utf_8_sig', header=False, index=False)

def convertKanjiDate2EnDate(kanji_date):
    s = kanji_date
    find_pattern = r"^(?P<m>\d*)月頃"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda date: '2021' + '-' + date.group('m') + '-1'
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    find_pattern = r"^(?P<m>\d*)月(?P<d>\d*)\D*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda date: '2021' + '-' + date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    find_pattern = r"^(?P<y>\d*)年(?P<m>\d*)月(?P<d>\d*)\D*"
    m = re.match(find_pattern, s)
    if m != None:
        replace_pattern = lambda date: date.group('y') + '-' + date.group('m') + '-' + date.group('d')
        en_date = re.sub(find_pattern, replace_pattern, s)
        tdate = datetime.datetime.strptime(en_date, '%Y-%m-%d')
        return tdate.strftime('%Y-%m-%d')

    return convertReiwa2Year(kanji_date)


# Get opendate csv
getOpenDateV2('./csv/patients_opendate_current.csv','/site/hoken/kansen/soumu/press/20200214_covid19_pr1.html')
#getOpenDateV2('./csv/patients_opendate_8.csv','/site/hoken/kansen/soumu/press/20220831.html')
#getOpenDateV2('./csv/patients_opendate_7.csv','/site/hoken/kansen/soumu/press/20220622.html')
#getOpenDate('./csv/patients_opendate_6.csv','/site/hoken/kansen/soumu/press/20220215.html')
#getOpenDate('./csv/patients_opendate_5.csv','/site/hoken/kansen/soumu/press/20220214.html')
#getOpenDate('./csv/patients_opendate_4.csv','/site/hoken/kansen/soumu/press/20210914.html')
#getOpenDate('./csv/patients_opendate_3.csv','/site/hoken/kansen/soumu/press/20210909.html')
#getOpenDate('./csv/patients_opendate_2.csv','/site/hoken/kansen/soumu/press/20210130.html')
#getOpenDate('./csv/patients_opendate_x.csv','/site/hoken/kansen/soumu/press/20201019.html')

# Load opendate csv
dateDf = pd.read_csv('./csv/patients_opendate_r040927.csv')
df9 = pd.read_csv('./csv/patients_opendate_current.csv')
dateDf = dateDf.append(df9)
df8 = pd.read_csv('./csv/patients_opendate_8.csv')
dateDf = dateDf.append(df8)
df7 = pd.read_csv('./csv/patients_opendate_7.csv')
dateDf = dateDf.append(df7)
df6 = pd.read_csv('./csv/patients_opendate_6.csv')
dateDf = dateDf.append(df6)
df5 = pd.read_csv('./csv/patients_opendate_5.csv')
dateDf = dateDf.append(df5)
df4 = pd.read_csv('./csv/patients_opendate_4.csv')
dateDf = dateDf.append(df4)
df3 = pd.read_csv('./csv/patients_opendate_3.csv')
dateDf = dateDf.append(df3)
df2 = pd.read_csv('./csv/patients_opendate_2.csv')
dateDf = dateDf.append(df2)
df1 = pd.read_csv('./csv/patients_opendate_1.csv')
dateDf = dateDf.append(df1)
print(dateDf)

# correct
#dateDf.loc[dateDf['first_case'] == 88023, 'opendate'] = '2022-02-09'
dateDf['first_case'] = dateDf['first_case'].astype('i8')
dateDf['last_case'] = dateDf['last_case'].astype('i8')

# Download patient csv
download_file = downlod_patient.Download_FullRecordes()

# Format
removeReturn(download_file,'./csv/remove_return.csv')
rejectMissing('./csv/remove_return.csv', './csv/rejected_youseisyaitiran.csv')
dfPat = pd.read_csv('./csv/rejected_youseisyaitiran.csv')
dfPat['caseNo'] = dfPat['caseNo'].astype('i8')

masterDf = pd.DataFrame(None,columns = ['caseNo','sex','age','onsetDate','fixDate','area','work','route','openDate','delete'])

for index, row in dateDf.iterrows():
    houDf = dfPat[(dfPat['caseNo'] >= row['first_case']) & (dfPat['caseNo'] <= row['last_case'])]
    houDf = houDf.assign(openDate=row['opendate'])
    houDf = houDf.assign(delete=0)
    masterDf = masterDf.append(houDf)

masterDf = masterDf.reindex(columns=['caseNo','sex','age','onsetDate','fixDate','openDate','area','work','route','delete'])
masterDf = masterDf.drop_duplicates(subset='caseNo')
masterDf = masterDf.sort_values('caseNo', ascending=True)

masterDf.loc[masterDf['age'] == '00歳','age']='10歳未満'
masterDf.loc[masterDf['age'] == '01～04歳','age']='10歳未満'
masterDf.loc[masterDf['age'] == '05～09歳','age']='10歳未満'
masterDf.loc[masterDf['age'] == '10～19歳','age']='10代'
masterDf.loc[masterDf['age'] == '20～29歳','age']='20代'
masterDf.loc[masterDf['age'] == '30～39歳','age']='30代'
masterDf.loc[masterDf['age'] == '40～49歳','age']='40代'
masterDf.loc[masterDf['age'] == '50～59歳','age']='50代'
masterDf.loc[masterDf['age'] == '60～64歳','age']='60代'
masterDf.loc[masterDf['age'] == '65～69歳','age']='60代'
masterDf.loc[masterDf['age'] == '70～79歳','age']='70代'
masterDf.loc[masterDf['age'] == '80～89歳','age']='80代'
print(masterDf)

masterDf.to_csv('./csv/patient.csv', encoding='utf_8_sig', header=True, index=False)
os.remove('./csv/rejected_youseisyaitiran.csv')
os.remove('./csv/remove_return.csv')
