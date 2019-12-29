import json
import requests


class Collection:
    def __init__(self):
        self.databaseItems = []
        self.customerProperty = []
        self.filter = 'renderItem'

    def getDataFromDatabase(self):
        data = json.loads(requests.get('https://sarginapi.herokuapp.com/renders').text);

        if self.filter == 'renderItem':
            for item in data:
                self.customerProperty.append({
                    'musteriAdi': item['data'].get('musteriAdi'),
                    'musteriEmail': item['data'].get('musteriEmail'),
                    'time': int(item.get('data').get('time'))
                })

                for element in item['data']['cizim']:
                    self.databaseItems.append(element);
        else:
            for element in data:
                if element['render'] == False:
                    for item in element['data']['cizim']:
                        self.databaseItems.append(item);

        print(self.customerProperty)

    def printElement(self):
        print(self.databaseItems);
        print('\n');


if __name__ == '__main__':
    element = Collection();
    element.getDataFromDatabase();
    element.printElement();
