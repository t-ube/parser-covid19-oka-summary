import csv
import pandas as pd
import datetime as dt
import os
import pathlib
import sys
import json

def getWeeklyMedian(df):
    writedata = []
    writedata.append(df[df['dow'] == 0]['全体'].median()) 
    writedata.append(df[df['dow'] == 1]['全体'].median()) 
    writedata.append(df[df['dow'] == 2]['全体'].median()) 
    writedata.append(df[df['dow'] == 3]['全体'].median()) 
    writedata.append(df[df['dow'] == 4]['全体'].median()) 
    writedata.append(df[df['dow'] == 5]['全体'].median()) 
    writedata.append(df[df['dow'] == 6]['全体'].median()) 
    return writedata

# 曜日ごとの中央値
def convertCsv2Json_PatientMedianWeekday(csv,out) :
    df = pd.read_csv(csv, header=0)

    writedata = {}

    df['indexDate'] = pd.to_datetime(df['openDate']).dt.strftime('%Y-%m-%d')
    df['openDate'] = pd.to_datetime(df['openDate'])
    #print(df['openDate'].dtype)
    df['dow'] = pd.to_datetime(df['indexDate']).dt.weekday
    df.set_index('indexDate', inplace=True)
    #print(type(df.index))
    #print(df.index)

    dtEnd = df['openDate'].max()
    dtBegin3month = dtEnd - dt.timedelta(days=90)
    dtBegin1week = dtEnd - dt.timedelta(days=7)

    writedata['baseday'] = {}
    writedata['baseday']['date'] = dtEnd.strftime('%Y-%m-%d')
    writedata['baseday']['weekday'] = dtEnd.weekday()

    writedata['1week'] = {}
    writedata['1week']['Begin'] = dtBegin1week.strftime('%Y-%m-%d')
    writedata['1week']['End'] = dtEnd.strftime('%Y-%m-%d')
    writedata['1week']['Median'] = getWeeklyMedian(df[df['openDate'] > dtBegin1week])

    writedata['3month'] = {}
    writedata['3month']['Begin'] = dtBegin3month.strftime('%Y-%m-%d')
    writedata['3month']['End'] = dtEnd.strftime('%Y-%m-%d')
    writedata['3month']['Median'] = getWeeklyMedian(df[df['openDate'] > dtBegin3month])

    print(writedata)

    # 情報の保存
    #wfile = open(out, 'w', encoding='utf8')
    #json.dump(writedata, wfile, ensure_ascii=False)
    #wfile.close()

def convertCsv2Csv_Group7daysPatient(csv,out) :
    df = pd.read_csv(csv, header=0)

    df['openDate'] = pd.to_datetime(df['openDate']).dt.strftime('%Y-%m-%d')
    #print(df['openDate'].dtype)
    df.set_index('openDate', inplace=True)
    #print(type(df.index))
    #print(df.index)

    for area in df.columns.values.tolist():
        df[area] = df[area].rolling(7).sum().fillna(0).astype('int64')

    print(df)

    df.to_csv(out, encoding='utf_8_sig', index=True)


def convertCsv2Csv_GroupTotalPatient(csv,out) :
    df = pd.read_csv(csv, header=0)

    df['openDate'] = pd.to_datetime(df['openDate']).dt.strftime('%Y-%m-%d')
    df.set_index('openDate', inplace=True)

    for area in df.columns.values.tolist():
        df[area] = df[area].cumsum().astype('int64')

    print(df)

    df.to_csv(out, encoding='utf_8_sig', index=True)

def convertCsv2Json_Group7daysPatient(csv,out) :
    df = pd.read_csv(csv, header=0)

    writedata = {}
    writedata['openDate'] = df['openDate'].tolist()

    df['openDate'] = pd.to_datetime(df['openDate']).dt.strftime('%Y-%m-%d')
    #print(df['openDate'].dtype)
    df.set_index('openDate', inplace=True)
    #print(type(df.index))
    #print(df.index)

    for area in df.columns.values.tolist():
        writedata[area] = df[area].rolling(7).sum().fillna(0).astype('int64').tolist()

    #print(writedata)

    # 情報の保存
    wfile = open(out, 'w', encoding='utf8')
    json.dump(writedata, wfile, ensure_ascii=False)
    wfile.close()

def convertCsv2Json_Group1dayPatient(csv,out) :
    df = pd.read_csv(csv, header=0)

    writedata = {}
    writedata['openDate'] = df['openDate'].tolist()

    df['openDate'] = pd.to_datetime(df['openDate']).dt.strftime('%Y-%m-%d')
    df.set_index('openDate', inplace=True)

    for area in df.columns.values.tolist():
        writedata[area] = df[area].astype('int64').tolist()

    #print(writedata)

    # 情報の保存
    wfile = open(out, 'w', encoding='utf8')
    json.dump(writedata, wfile, ensure_ascii=False)
    wfile.close()

"""
#if os.path.exists('./data/area-patient-daily.csv') == False:
#    print('Not found: data/area-patient-daily.csv')
#    sys.exit(1)

#convertCsv2Csv_GroupTotalPatient('./data/area-patient-daily.csv', './data/area-patient-total.csv')
#convertCsv2Csv_Group7daysPatient('./data/area-patient-daily.csv', './data/area-patient-7days.csv')
#convertCsv2Csv_Group7daysPatient('./data/oka-patient-age-daily.csv', './data/oka-patient-age-7days.csv')
#convertCsv2Csv_GroupTotalPatient('./data/oka-patient-age-daily.csv', './data/oka-patient-age-total.csv')
#convertCsv2Csv_Group7daysPatient('./data/mmy-patient-age-daily.csv', './data/mmy-patient-age-7days.csv')
#convertCsv2Csv_GroupTotalPatient('./data/mmy-patient-age-daily.csv', './data/mmy-patient-age-total.csv')
convertCsv2Csv_Group7daysPatient('./data/isg-patient-age-daily.csv', './data/isg-patient-age-7days.csv')
convertCsv2Csv_GroupTotalPatient('./data/isg-patient-age-daily.csv', './data/isg-patient-age-total.csv')
#convertCsv2Json_PatientMedianWeekday('./data/area-patient-daily.csv', './data/dow.csv')
#convertCsv2Csv_GroupTotalPatient('./data/work-patient-daily.csv', './data/work-patient-total.csv')
#convertCsv2Json_Group7daysPatient('./data/area-patient-daily.csv', './data/area-patient-7days.json')
#convertCsv2Json_Group1dayPatient('./data/area-patient-daily.csv', './data/area-patient-daily.json')
sys.exit(0)
"""
