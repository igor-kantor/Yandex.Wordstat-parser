# YandexWordstatAPI
Simple small class for parsing data from WordStat via yandex direct api

## Installing YandexWordstatAPI
```console
$ python -m pip install YandexWordStatAPI
```

## Docs
```python
from YandexWordstatAPI.WordStatAPI import *
import time 


'''
Yandex sandbox url = https://api-sandbox.direct.yandex.ru/v4/json/
Yandex full access url = https://api.direct.yandex.ru/v4/json/
'''
url ='https://api-sandbox.direct.yandex.ru/v4/json/'  # api url 
token = 'AgAAAAAX1GmLIIX9s4uEoSNiSEyjjxTsAHZ0p8w' # Token to access Yandex.Direct API
username = 'yandex.username' # Username to get points value 

API = WordStatAPI(url, token, username)

phrases = [
    'фотошоп', 
    'photoshop'
]

exclude = [
    '-купить', 
    '-дешево',
    '-скачать',
    '-бесплатно'
    ]
geo = [] # Can be let empty

data = API.compose_data(phrases, exclude) # Compose data with exclude phrases

# Methods
units = API.get_client_units() # Get client units. ref: https://yandex.ru/dev/direct/doc/dg-v4/reference/GetClientsUnits.html
print(f"You have {units['data'][0]['UnitsRest']}")

report_id = API.create_report(data, geo)['data'] # Create new report, it will be redy in ~2 minutes. ref: https://yandex.ru/dev/direct/doc/dg-v4/reference/CreateNewWordstatReport.html
print(f"The report wit id {report_id} is creating")

report_list = API.get_report_list() # Get report list, you can wait til the report will be ready, or just check it later. ref: https://yandex.ru/dev/direct/doc/dg-v4/reference/GetWordstatReportList.html
last_report = report_list['data'][-1]
while lastReport['StatusReport'] != 'Done':
    if lastReport['StatusReport'] == 'Failed':
        raise Exception('Failed to create report')
    else:
        print('Report is creating...')
        lastReport = API.get_report_list()['data'][-1]
        time.sleep(2)

report = API.readReport(report_id) # Read report data by its id. ref: https://yandex.ru/dev/direct/doc/dg-v4/reference/GetWordstatReport.html
API.save_report_to_txt(report, searched_also_flag=True) # Save all data to txt, can be undone if not necessary 

response = API.delete_report(report_id) # Delete Wordstat report, it can be done when you reach report number limit(5 reports)
if response['data'] == 1:
    print(f'Report with id {report_id} was successfully deleted')
```
