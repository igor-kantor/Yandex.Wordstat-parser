import urllib.request
import urllib.error
import json
import warnings


class WordstatParser:
    def __init__(self, url, token, username=None):
        self.url = url
        self.token = token
        self.username = username

    def __checkData(self, response, methode):
        if 'data' in response:
            raise Exception(f'Failed to receive right data in {methode}')
            return False
        else:
            return response

    def getClientUnits(self):
        if self.username is None:
            warnings.warn("You didn't specify user login to use this method.")
            return None
        else:
            data = {
                'method': 'GetClientsUnits',
                'token': self.token,
                'param': [self.username]
            }
            data = json.dumps(data, ensure_ascii=False).encode('utf8')
            request = urllib.request.urlopen(self.url, data)
            response = json.loads(request.read().decode('utf8'))
            return self.__checkData(response, 'getClientUnits')

    def createReport(self, phrases, geo=[]):
        data = {
            'method': 'CreateNewWordstatReport',
            'token': self.token,
            'param': {
                'Phrases': phrases,
                'GeoID': geo
                }
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url, data)
        response = json.loads(request.read().decode('utf8'))
        return self.__checkData(response, 'createReport')
    
    def getReportList (self):
        data = {
            'method': 'GetWordstatReportList',
            'token': self.token    
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url, data)
        response = json.loads(request.read().decode('utf8'))
        return self.__checkData(response, 'getReportList')
        
    def readReport (self, reportID):
        data = {
            'method': 'GetWordstatReport',
            'token': self.token,
            'param': reportID
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url, data)
        response = json.loads(request.read().decode('utf8'))
        return self.__checkData(response, 'readReport')
    
    def deleteReport (self, reportID):
        data = {
            'method': 'DeleteWordstatReport',
            'token': self.token,
            'param': reportID
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url, data)
        response = json.loads(request.read().decode('utf8'))
        return self.__checkData(response, 'deleteReport')

    def saveReportToTxt (self, report, rightCol):
        if self.__checkData(report, 'saveReportToTxt'):
            phrases = open('phrases_left.txt', 'w')
            shows = open('shows_left.txt', 'w')
            for i in range(len(report['data'])):
                for j in report['data'][i]['SearchedWith']:
                    phraseToReport = str(j['Phrase'])
                    phrases.write(phraseToReport+'\n')
                    showsToReport = str(j['Shows'])
                    shows.write(showsToReport+'\n')
            phrases.close()
            shows.close()
            if rightCol:
                phrases = open('phrases_right.txt', 'w')
                shows = open('shows_right.txt', 'w')
                for i in range(len(report['data'])):
                    for j in report['data'][i]['SearchedAlso']:
                        phraseToReport = str(j['Phrase'])
                        phrases.write(phraseToReport+'\n')
                        showsToReport = str(j['Shows'])
                        shows.write(showsToReport+'\n')
                phrases.close()
                shows.close()
