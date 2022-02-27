import requests
import json
import warnings


class WordStatAPI:
    def __init__(self, url, token, username=None):
        self.url = url
        self.token = token
        self.username = username

    def compose_data(self, phrases, exclude_phrases):
        data = []
        for phrase in phrases:
            for j in range(len(exclude_phrases)):
                phrase += ' ' + exclude_phrases[j]
            data.append(phrase)
        return data

    def __check_data(self, response, methode):
        if 'data' not in response:
            raise Exception(f'Failed to receive right data in {methode}')
            return False
        else:
            return response

    def get_client_units(self):
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
            r = requests.get(self.url, data).json()
            return self.__check_data(r, 'get_client_units')

    def create_report(self, phrases, geo=[]):
        data = {
            'method': 'CreateNewWordstatReport',
            'token': self.token,
            'param': {
                'Phrases': phrases,
                'GeoID': geo
            }
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        r = requests.get(self.url, data).json()
        return self.__check_data(r, 'create_report')

    def get_report_list(self):
        data = {
            'method': 'GetWordstatReportList',
            'token': self.token
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        r = requests.get(self.url, data).json()
        return self.__check_data(r, 'get_report_list')

    def read_report(self, report_id):
        data = {
            'method': 'GetWordstatReport',
            'token': self.token,
            'param': report_id
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        r = requests.get(self.url, data).json()
        return self.__check_data(r, 'read_report')

    def delete_report(self, report_id):
        data = {
            'method': 'DeleteWordstatReport',
            'token': self.token,
            'param': report_id
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        r = requests.get(self.url, data).json()
        return self.__check_data(r, 'delete_report')

    def save_report_to_txt(self, report, searched_also_flag=True):
        if self.__check_data(report, 'save_report_to_txt'):
            searched_with = open('searched_with.txt', 'w')
            searched_also = open('searched_also.txt', 'w')
            for phrase in report['data']:
                for j in phrase['SearchedWith']:
                    item = str(j['Phrase']) + ": " + str(j['Shows']) + "\n"
                    searched_with.write(item)
                if searched_also_flag:
                    for j in phrase['SearchedAlso']:
                        item = str(j['Phrase']) + ": " + str(j['Shows']) + "\n"
                        searched_also.write(item)
            searched_with.close()
            searched_also.close()

    def get_regions(self):
        data = {
            'method': 'GetRegions',
            'token': self.token,
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        r = requests.get(self.url, data).json()
        return self.__check_data(r, 'get_regions')
