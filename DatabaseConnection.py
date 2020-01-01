import json
import requests


class Collection:
    def __init__(self):
        self.databaseItems = []
        self.customerProperty = []
        self.filter = 'renderItem'
        self.renderedData = {}
        self.shortedData = []

    def getDataFromDatabase(self):
        data = json.loads(requests.get('https://sarginapi.herokuapp.com/renders').text);

        if self.filter == 'renderItem':
            for item in data:
                if item['data'].get('rendered'):
                    self.databaseItems = []
                    for element in item['data']['cizim']:
                        self.databaseItems.append(element);

                    self.customerProperty.append({
                        'databaseId': item['data'].get('wixId'),
                        'musteriAdi': item['data'].get('musteriAdi'),
                        'musteriEmail': item['data'].get('musteriEmail'),
                        'time': int(item.get('data').get('time')),
                        'databaseItems': self.databaseItems
                    });

        if len(self.customerProperty) > 1:
            for i in range(1, len(self.customerProperty)):
                if self.customerProperty[i].get('time') > self.customerProperty[i - 1].get('time'):
                    self.shortedData.append(self.customerProperty[i - 1])
                else:
                    self.shortedData.append(self.customerProperty[i])
        elif len(self.customerProperty) != 0:
            self.shortedData.append(self.customerProperty[0])

        return len(self.shortedData) == 0

    def printElement(self):
        print(self.databaseItems);
        print('\n');

    def changeRenderStatus(self, id):
        requests.post('https://sarginapi.herokuapp.com/renders/update/' + id, {'renderedStatus': False})


if __name__ == '__main__':
    element = Collection();
    element.getDataFromDatabase()
