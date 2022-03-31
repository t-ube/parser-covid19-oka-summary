import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def DownloadAllCSV(excludeList):
    file_list = []

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
            if file_name not in excludeList:
                file_href = href
                print(file_name)
                file_list.append(file_name)
                download_url = domain + file_href
                download_file = './csv/' + file_name
                if os.path.isfile(download_file):
                    print("CSV downloaded skip: csv/" + file_name)
                else:
                    urllib.request.urlretrieve(download_url, download_file)
                    print("CSV downloaded at: csv/" + file_name)
    
    return file_list

def Download(excludeList):
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
            if file_name not in excludeList:
                file_href = href
                print(file_name)
                break

    if file_name == None:
        return None
    
    download_url = domain + file_href
    download_file = './csv/' + file_name
    if os.path.isfile(download_file):
        print("CSV downloaded skip: csv/" + file_name)
    else:
        urllib.request.urlretrieve(download_url, download_file)
        print("CSV downloaded at: csv/" + file_name)
    return file_name

def Union(dest,unionList):
    data_list = []
    for filename in unionList:
        data_list.append(pd.read_csv(
        filepath_or_buffer='./csv/'+filename,
        encoding="ms932", sep=","))
        df = pd.concat(data_list, sort=False)
        df.to_csv(dest,index=False)
    return

def Download_FullRecordes():
    excludeList = ['youseishaitiran_1-50000.csv']
    download_list = DownloadAllCSV(excludeList)
    unionList = []
    if download_list != None:
        for l in download_list:
            unionList.append(l)
    for l in excludeList:
        unionList.append(l)
    Union("./csv/union_youseishaitiran.csv", unionList)
    return "./csv/union_youseishaitiran.csv"
