# Подлючаем класс парсера WordstatParser, импортируем необходимые модули
from wsparser import WordstatParser
import time

##################################################################################
# Вводим исходные данные для парсинга
##################################################################################

# Задаем URL адрес API Яндекс.Директа
# Адрес песочницы: url ='https://api-sandbox.direct.yandex.ru/v4/json/' 
# Адрес полного доступа: url ='https://api.direct.yandex.ru/v4/json/'
url ='https://api-sandbox.direct.yandex.ru/v4/json/' 
# Указываем свой токен на доступ к API Яндекс.Директ
token = 'AgAAAAAX1GmLIIX9s4uEoSNiSEyjjxTsAHZ0p8w'
# Указываем логин своей учетной записи от Яндекс.Директ
userName = 'yandex.username'

# Пишем список общих минус-слов, как в примере (со знаком "-")
minusWords = [
    '-купить', 
    '-дешево',
    '-скачать',
    '-бесплатно'
    ]

# Пишем список фраз, по которым будем парсить    
phrases = [
    'фотошоп', 
    'photoshop'
    ]

# Указываем регион, при необходимости (можно оставить пустым)        
geo = []

##################################################################################
# Код скрипта парсинга
##################################################################################

# Добавляем минус-слова ко всем фразам
data = []
for i in range(len(phrases)):
    data.append(phrases[i])
    for j in range(len(minusWords)):
        data[i] += ' '+minusWords[j]

# Создаем парсер
parser = WordstatParser(url, token, userName)

try:
    # Запрашиваем кол-во оставшихся баллов Яндекс.Директ API
    units = parser.getClientUnits()
    if 'data' in units:
        print ('>>> Баллов осталось: ', units['data'][0]['UnitsRest'])
    else:
        raise Exception('Не удалось получить баллы', units)

    # Отправляем запрос на создание нового отчета на сервере Яндекс.Директ
    response = parser.createReport(data, geo)
    if 'data' in response:
        reportID = response['data']
        print ('>>> Создается отчет с ID = ', reportID)
    else:
        raise Exception('Не удалось создать отчет', response)
        
    # Проверяем список отчетов на сервере. Должен появиться новый. Ожидаем его готовности
    reportList = parser.getReportList()
    if 'data' in reportList:
        lastReport = reportList['data'][len(reportList['data'])-1]
        i = 0
        while lastReport['StatusReport'] != 'Done':
            print ('>>> Подготовка отчета, ждите ... ('+str(i)+')')
            time.sleep(2)
            reportList = parser.getReportList()
            lastReport = reportList['data'][len(reportList['data'])-1]
            i+=1
        print ('>>> Отчет ID = ', lastReport['ReportID'], ' получен!')
    else:
        raise Exception('Не удалось прочитать список отчетов', reportList)

    # Читаем отчет
    report = parser.readReport(reportID)
    if 'data' in report:
        # Сохраняем результаты парсинга в файлы (отдельно фразы, отдельно частотности). 
        # Если rightCol == True, будет сохраняться правая колонка Яндекс.Вордстат (в дополнение к левой)
        parser.saveReportToTxt(report, True)
        print ('>>> Результаты парсига успешно сохранены в файлы!')
    else:
        raise Exception('Не удалось прочитать отчет', report)
    
    # Удаляем на сервере Яндекс.Директ новый отчет (он больше не нужен)
    report = parser.deleteReport(reportID)
    if 'data' in report:
        print ('>>> Отчет с ID = ', reportID, ' успешно удален с сервера Яндекс.Директ')
    else:
        raise Exception('Не удалось удалить отчет', report)
    
    print ('>>> Все готово!')
    
# Все готово! Ищем файлы "phrases_lef.txt" и "shows_left.txt" с резльтатами парсинга в директории этого скрипта
except Exception as e:
    print ('>>> Поймано исключение:', e)