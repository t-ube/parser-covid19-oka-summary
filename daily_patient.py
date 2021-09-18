import requests
import urllib.request

from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import pathlib
import sys
import datetime
from datetime import timedelta

def convertCsv2DailyWorkerCsv(source,daily):
    df = pd.read_csv(source, header=0, parse_dates=["openDate"])
    df = df[df['delete'] == 0]

    print(df['openDate'])
    print(min(df['openDate']))

    minDate = (pd.to_datetime(min(df['openDate']))-timedelta(days=14)).strftime('%Y-%m-%d')
    maxDate = max(df['openDate'])

    daterange = pd.date_range(minDate, maxDate)
    print(daterange)

    workDf = df.groupby(['openDate','work']).count()
    #print(areaDf.caseNo)

    print(df.groupby(['work']).count())

    file = open(daily, 'w', encoding='utf-8-sig', newline="")
    writer = csv.writer(file)

    writeHeader = ['openDate']

    for _name in df.groupby(['work']):
        writeHeader.append(_name[0])

    writeHeader.append('全体')

    #print(writeHeader)
    writer.writerow(writeHeader)

    for date in daterange:
        dateText = date.strftime('%Y-%m-%d')
        #print(dateText)
        writeData = [dateText]
        for _name, _df in df.groupby(['work']):
            localDf = ((df['openDate'] == dateText) & (df['work'] == _name))
            #print(localDf.sum())
            writeData.append(localDf.sum())
        dfAll = (df['openDate'] == dateText)
        writeData.append(dfAll.sum())
        writer.writerow(writeData)
        
    file.close()

def convertCsv2DailyCsv(source,daily,first_date,fix_date):
    df = pd.read_csv(source, header=0, parse_dates=["openDate"])
    df = df[df['delete'] == 0]

    print(df['openDate'])
    print('min:')
    print(min(df['openDate']))

    minDate = (pd.to_datetime(min(df['openDate']))-timedelta(days=14)).strftime('%Y-%m-%d')
    print('max:')
    maxDate = max(df['openDate'])

    daterange = pd.date_range(first_date, fix_date)
    #daterange = pd.date_range(minDate, maxDate)
    print(daterange)

    areaDf = df.groupby(['openDate','area']).count()
    #print(areaDf.caseNo)

    print(df.groupby(['area']).count())

    file = open(daily, 'w', encoding='utf-8-sig', newline="")
    writer = csv.writer(file)

    writeHeader = ['openDate']

    for _name in df.groupby(['area']):
        writeHeader.append(_name[0])

    writeHeader.append('沖縄本島')
    writeHeader.append('宮古諸島')
    writeHeader.append('八重山諸島')
    writeHeader.append('全体')

    #print(writeHeader)
    writer.writerow(writeHeader)

    for date in daterange:
        dateText = date.strftime('%Y-%m-%d')
        #print(dateText)
        writeData = [dateText]
        for _name, _df in df.groupby(['area']):
            localDf = ((df['openDate'] == dateText) & (df['area'] == _name))
            #print(localDf.sum())
            writeData.append(localDf.sum())
        dfOKA = ((df['openDate'] == dateText) & ((df['area'] == '北部保健所管内') | (df['area'] == '名護市') | (df['area'] == '中部保健所管内') | (df['area'] == 'うるま市') | (df['area'] == '沖縄市') | (df['area'] == '南部保健所管内') | (df['area'] == '宜野湾市') | (df['area'] == '浦添市') | (df['area'] == '那覇市') | (df['area'] == '豊見城市') | (df['area'] == '南城市') | (df['area'] == '糸満市')))
        dfMMY = ((df['openDate'] == dateText) & ((df['area'] == '宮古島市') | (df['area'] == '宮古保健所管内')))
        dfISG = ((df['openDate'] == dateText) & ((df['area'] == '石垣市') | (df['area'] == '八重山保健所管内')))
        dfAll = (df['openDate'] == dateText)
        writeData.append(dfOKA.sum())
        writeData.append(dfMMY.sum())
        writeData.append(dfISG.sum())
        writeData.append(dfAll.sum())
        writer.writerow(writeData)
        
    file.close()

def convertCsv2DailyOKACsv(source,dest):
    df = pd.read_csv(source, header=0, parse_dates=["openDate"])
    dfOKA = df[(((df['area'] == '北部保健所管内') | (df['area'] == '名護市') | (df['area'] == '中部保健所管内') | (df['area'] == 'うるま市') | (df['area'] == '沖縄市') | (df['area'] == '南部保健所管内') | (df['area'] == '宜野湾市') | (df['area'] == '浦添市') | (df['area'] == '那覇市') | (df['area'] == '豊見城市') | (df['area'] == '南城市') | (df['area'] == '糸満市')))]
    print(dfOKA)
    dfOKA.to_csv(dest, encoding='utf_8_sig', index=False)

def convertCsv2DailyMMYCsv(source,dest):
    df = pd.read_csv(source, header=0, parse_dates=["openDate"])
    dfMMY = df[(((df['area'] == '宮古島市') | (df['area'] == '宮古保健所管内')))]
    print(dfMMY)
    dfMMY.to_csv(dest, encoding='utf_8_sig', index=False)

def convertCsv2DailyISGCsv(source,dest):
    df = pd.read_csv(source, header=0, parse_dates=["openDate"])
    dfISG = df[(((df['area'] == '石垣市') | (df['area'] == '八重山保健所管内')))]
    print(dfISG)
    dfISG.to_csv(dest, encoding='utf_8_sig', index=False)

def convertCsv2DailyAgeCsv(source,daily,first_date,fix_date):
    df = pd.read_csv(source, header=0, parse_dates=["openDate"])
    df = df[df['delete'] == 0]

    print(df['openDate'])
    print(min(df['openDate']))

    minDate = (pd.to_datetime(min(df['openDate']))-timedelta(days=14)).strftime('%Y-%m-%d')
    #maxDate = max(df['openDate'])

    daterange = pd.date_range(first_date, fix_date)
    #daterange = pd.date_range(minDate, maxDate)
    print(daterange)

    ageDf = df.groupby(['openDate','age']).count()
    #print(areaDf.caseNo)

    print(df.groupby(['age']).count())

    file = open(daily, 'w', encoding='utf-8-sig', newline="")
    writer = csv.writer(file)

    writeHeader = ['openDate']

    for _name in df.groupby(['age']):
        writeHeader.append(_name[0])

    #print(writeHeader)
    writer.writerow(writeHeader)

    for date in daterange:
        dateText = date.strftime('%Y-%m-%d')
        #print(dateText)
        writeData = [dateText]
        for _name, _df in df.groupby(['age']):
            localDf = ((df['openDate'] == dateText) & (df['age'] == _name))
            #print(localDf.sum())
            writeData.append(localDf.sum())
        writer.writerow(writeData)
        
    file.close()

"""
firstdate = '2020-02-14'
fixdate = '2021-04-26'

convertCsv2DailyCsv('./data/patient.csv', './data/area-patient-daily.csv', firstdate, fixdate)


if os.path.exists('./data/patient.csv') == False:
    print('Not found: data/patient.csv')
    sys.exit(1)

#convertCsv2DailyWorkerCsv('./data/patient.csv', './data/work-patient-daily.csv')
#convertCsv2DailyOKACsv('./data/patient.csv', './data/oka-patient-daily.csv')
#convertCsv2DailyMMYCsv('./data/patient.csv', './data/mmy-patient-daily.csv')
#convertCsv2DailyISGCsv('./data/patient.csv', './data/isg-patient-daily.csv')
#convertCsv2DailyAgeCsv('./data/oka-patient-daily.csv', './data/oka-patient-age-daily.csv')
#convertCsv2DailyAgeCsv('./data/mmy-patient-daily.csv', './data/mmy-patient-age-daily.csv')
#convertCsv2DailyAgeCsv('./data/isg-patient-daily.csv', './data/isg-patient-age-daily.csv','2021-01-23')
#convertCsv2DailyCsv('./data/patient.csv', './data/area-patient-daily.csv','2021-01-23')
sys.exit(0)
"""
