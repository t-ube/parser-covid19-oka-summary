import pandas as pd
import datetime
import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

dt_now = datetime.datetime.utcnow()
# UTC+9
dt_20 = dt_now.replace(hour=11, minute=0, second=0)

if dt_now > dt_20:
    fixdate = dt_now.strftime('%Y-%m-%d')
    before60day= dt_now + datetime.timedelta(days=-60)
else:
    tempdate = dt_now + datetime.timedelta(days=-1)
    fixdate = tempdate.strftime('%Y-%m-%d')
    before60day= dt_now + datetime.timedelta(days=-60)

firstdate = '2020-02-14'
filterdate = before60day.strftime('%Y-%m-%d')

def getPatientsData(source):
    df = pd.read_csv(source, encoding='utf_8_sig', sep=",")
    sortDf = df.sort_values('caseNo', ascending=False)
    dropDf = sortDf.drop(columns=['caseNo', 'onsetDate', 'work', 'route', 'delete'])
    dropDf['fixDate'] = dropDf['fixDate']+'T08:00:00.000Z'
    dropDf['状態'] = None
    dropDf['退院'] = None
    dropDf['備考'] = None
    dropDf.rename(columns={'sex': '性別', 'age':'年代', 'fixDate':'確定日', 'openDate':'date', 'area':'居住地'}, inplace=True)
    saveDf = dropDf.reindex(columns=['確定日','居住地','年代','性別','状態','退院','備考','date'])
    return json.loads(saveDf.to_json(orient='records', force_ascii=False))

def getPatientsDataV2(source):
    df = pd.read_csv(source, encoding='utf_8_sig', sep=",")
    sortDf = df.sort_values('caseNo', ascending=False)
    dropDf = sortDf.drop(columns=['caseNo', 'onsetDate', 'work', 'route', 'delete'])
    dropDf['fixDate'] = dropDf['fixDate']+'T08:00:00.000Z'
    dropDf.rename(columns={'sex': '性別', 'age':'年代', 'fixDate':'確定日', 'openDate':'date', 'area':'居住地'}, inplace=True)
    saveDf = dropDf.reindex(columns=['確定日','居住地','年代','性別','date'])
    return json.loads(saveDf.to_json(orient='records', force_ascii=False))

def getPatientsDataV3(source,start_date):
    df = pd.read_csv(source, encoding='utf_8_sig', sep=",")
    dayFilterDf = df[df['fixDate'] >= start_date]
    sortDf = dayFilterDf.sort_values('caseNo', ascending=False)
    dropDf = sortDf.drop(columns=['caseNo', 'onsetDate', 'work', 'route', 'delete'])
    dropDf['fixDate'] = dropDf['fixDate']+'T08:00:00.000Z'
    dropDf.rename(columns={'sex': '性別', 'age':'年代', 'fixDate':'確定日', 'openDate':'date', 'area':'居住地'}, inplace=True)
    saveDf = dropDf.reindex(columns=['確定日','居住地','年代','性別','date'])
    return json.loads(saveDf.to_json(orient='records', force_ascii=False))

def getPatientsSummaryData(source,start_date,fix_date):
    df = pd.read_csv(source, header=0, parse_dates=["openDate"])
    df = df[df['delete'] == 0]
    daterange = pd.date_range(start_date, fix_date)
    saveDf = pd.DataFrame({'日付':[], '小計':[] }, index=[])
    for date in daterange:
        dateText = date.strftime('%Y-%m-%d')
        localDf = ((df['openDate'] == dateText))
        saveDf = saveDf.append({'日付': dateText,'小計':localDf.sum()}, ignore_index=True)
    saveDf['日付'] = saveDf['日付']+'T08:00:00.000Z'
    saveDf['小計'] = saveDf['小計'].astype(int)
    return json.loads(saveDf.to_json(orient='records', force_ascii=False))

def getMainSummaryChildren(source):
    src = open(source, 'r')
    json_load = json.load(src)
    writedata = []
    writedata.append({})
    writedata[0]['attr'] = '陽性患者数'
    writedata[0]['value'] = json_load['patient']
    writedata[0]['children'] = []
    writedata[0]['children'].append({})
    writedata[0]['children'][0]['attr'] = '入院中'
    writedata[0]['children'][0]['value'] = json_load['hospitalize']
    writedata[0]['children'][0]['children'] = []
    writedata[0]['children'][0]['children'].append({})
    writedata[0]['children'][0]['children'][0]['attr'] = '軽症・中等症'
    writedata[0]['children'][0]['children'][0]['value'] = json_load['hospitalize'] - json_load['severe']
    writedata[0]['children'][0]['children'].append({})
    writedata[0]['children'][0]['children'][1]['attr'] = '重症'
    writedata[0]['children'][0]['children'][1]['value'] = json_load['severe']
    writedata[0]['children'].append({})
    writedata[0]['children'][1]['attr'] = '宿泊療養'
    writedata[0]['children'][1]['value'] = json_load['hotel']
    writedata[0]['children'].append({})
    writedata[0]['children'][2]['attr'] = '自宅療養'
    writedata[0]['children'][2]['value'] = json_load['home']
    writedata[0]['children'].append({})
    writedata[0]['children'][3]['attr'] = '入院等調整中'
    writedata[0]['children'][3]['value'] = json_load['wait']
    writedata[0]['children'].append({})
    writedata[0]['children'][4]['attr'] = '死亡'
    writedata[0]['children'][4]['value'] = json_load['dead']
    writedata[0]['children'].append({})
    writedata[0]['children'][5]['attr'] = '退院'
    writedata[0]['children'][5]['value'] = json_load['release']

    return writedata

def convertCsv2StopCovid19Json(patients_source,summary_source,dest,start_date,fix_date):
    dt_now = datetime.datetime.now()
    mydict = {
        'patients': {
            'date': dt_now.strftime('%Y/%m/%d %H:%M'),
            'data': getPatientsDataV3(patients_source,start_date)
        },
        'patients_summary': {
            'date': dt_now.strftime('%Y/%m/%d %H:%M'),
            'data': getPatientsSummaryData(patients_source,start_date,fix_date)
        },
        'inspections_summary': {
            'date': dt_now.strftime('%Y/%m/%d %H:%M')
        },
        'lastUpdate': dt_now.strftime('%Y/%m/%d %H:%M'),
        'main_summary': {
            'date': dt_now.strftime('%Y/%m/%d %H:%M'),
            'attr': '検査実施人数',
            'value': 0,
            'children': getMainSummaryChildren(summary_source)
        }
    }

    file = open(dest, 'w', encoding='utf-8-sig')
    #json.dump(mydict, file, indent=4, ensure_ascii=False)
    json.dump(mydict, file, ensure_ascii=False)
    file.close()

convertCsv2StopCovid19Json('./csv/patient.csv','./data/summary-oka.json','./data/stopcovid19-data.json', filterdate, fixdate)
