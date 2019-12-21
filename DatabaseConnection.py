import json
import requests


class Collection:
    def __init__(self):
        self.databaseItems = [];

    def getDataFromDatabase(self):
        data = json.loads(requests.get('https://sarginapi.herokuapp.com/renders').text);

        for item in data:
            for element in item['data']['cizim']:
                self.databaseItems.append(element);

    def printElement(self):
        print(self.databaseItems);
        print('\n');


if __name__ == '__main__':
    element = Collection();
    element.getDataFromDatabase();
    element.printElement();
