import os
import sys
import datetime
import json

import daily_patient
import group_patient

os.chdir(os.path.dirname(os.path.abspath(__file__)))

dt_now = datetime.datetime.now()
dt_20 = dt_now.replace(hour=20, minute=0, second=0)

if dt_now > dt_20:
    fixdate = dt_now.strftime('%Y-%m-%d')
else:
    tempdate = dt_now + datetime.timedelta(days=-1)
    fixdate = tempdate.strftime('%Y-%m-%d')

print('fixdate:'+fixdate)

firstdate = '2020-02-14'

writedata = {}
writedata['firstdate'] = firstdate
writedata['fixdate'] = fixdate

daily_patient.convertCsv2DailyCsv('./csv/patient.csv', './data/area-patient-daily.csv', firstdate, fixdate)
daily_patient.convertCsv2DailyOKACsv('./csv/patient.csv', './csv/oka-patient-daily.csv')
daily_patient.convertCsv2DailyMMYCsv('./csv/patient.csv', './csv/mmy-patient-daily.csv')
daily_patient.convertCsv2DailyISGCsv('./csv/patient.csv', './csv/isg-patient-daily.csv')
daily_patient.convertCsv2DailyAgeCsv('./csv/oka-patient-daily.csv', './data/oka-patient-age-daily.csv', firstdate, fixdate)
daily_patient.convertCsv2DailyAgeCsv('./csv/mmy-patient-daily.csv', './data/mmy-patient-age-daily.csv', firstdate, fixdate)
daily_patient.convertCsv2DailyAgeCsv('./csv/isg-patient-daily.csv', './data/isg-patient-age-daily.csv', firstdate, fixdate)

group_patient.convertCsv2Csv_Group7daysPatient('./data/area-patient-daily.csv', './data/area-patient-7days.csv')
group_patient.convertCsv2Csv_GroupTotalPatient('./data/area-patient-daily.csv', './data/area-patient-total.csv')
group_patient.convertCsv2Csv_Group7daysPatient('./data/oka-patient-age-daily.csv', './data/oka-patient-age-7days.csv')
group_patient.convertCsv2Csv_GroupTotalPatient('./data/oka-patient-age-daily.csv', './data/oka-patient-age-total.csv')
group_patient.convertCsv2Csv_Group7daysPatient('./data/mmy-patient-age-daily.csv', './data/mmy-patient-age-7days.csv')
group_patient.convertCsv2Csv_GroupTotalPatient('./data/mmy-patient-age-daily.csv', './data/mmy-patient-age-total.csv')
group_patient.convertCsv2Csv_Group7daysPatient('./data/isg-patient-age-daily.csv', './data/isg-patient-age-7days.csv')
group_patient.convertCsv2Csv_GroupTotalPatient('./data/isg-patient-age-daily.csv', './data/isg-patient-age-total.csv')

# 情報の保存
update_wfile = open('./data/patient-time.json', 'w', encoding='utf8')
json.dump(writedata, update_wfile, ensure_ascii=False, indent=2)
update_wfile.close()

os.remove('./csv/oka-patient-daily.csv')
os.remove('./csv/mmy-patient-daily.csv')
os.remove('./csv/isg-patient-daily.csv')
os.remove('./csv/patient.csv')

sys.exit(0)