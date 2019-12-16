import json, urllib.request, urllib.error
class WordstatParser:
    def __init__(self, url, token, username):
        self.url = url
        self.token = token
        self.username = username
        
    def getClientUnits(self):
        data = {
            'method': 'GetClientsUnits',
            'token': self.token,
            'param': [self.username]
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url,data) 
        response = json.loads(request.read().decode('utf8'))
        return response

    def createReport(self, phrases, geo = []):
        data = {
            'method': 'CreateNewWordstatReport',
            'token': self.token,
            'param': {
                'Phrases': phrases,
                'GeoID': geo
                }
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url,data) 
        response = json.loads(request.read().decode('utf8'))
        return response
    
    def getReportList (self):
        data = {
            'method': 'GetWordstatReportList',
            'token': self.token    
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url,data) 
        response = json.loads(request.read().decode('utf8'))
        return response
        
    def readReport (self, reportID):
        data = {
            'method': 'GetWordstatReport',
            'token': self.token,
            'param': reportID
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url,data) 
        response = json.loads(request.read().decode('utf8'))
        return response
    
    def deleteReport (self, reportID):
        data = {
            'method': 'DeleteWordstatReport',
            'token': self.token,
            'param': reportID
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        request = urllib.request.urlopen(self.url,data) 
        response = json.loads(request.read().decode('utf8'))
        return response

    def saveReportToTxt (self, report, leftCol, rightCol):
        if leftCol == True:
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
        if rightCol == True:
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

        