import json
import requests
import pyrebase


class Collection:
    def __init__(self):
        self.databaseItems = []
        self.customerProperty = []
        self.filter = 'renderItem'
        self.renderedData = {}
        self.shortedData = []

        self.config = {
            "apiKey": "AIzaSyDN2GcZbIwk5wpW-7KkWYPRN_Yf1KBJnQk",
            "authDomain": "blender-44440.firebaseapp.com",
            "databaseURL": "https://blender-44440.firebaseio.com",
            "projectId": "blender-44440",
            "storageBucket": "",
            "messagingSenderId": "625093549043",
            "appId": "1:625093549043:web:fb06aaeae958bd44a15086"
        }

        self.firebase = pyrebase.initialize_app(self.config)

    def getDataFromDatabase(self):
        # data = json.loads(requests.get('https://sarginapi.herokuapp.com/renders').text);
        db = self.firebase.database()

        blenderModel = db.child("wixData").get().val()

        if self.filter == 'renderItem':
            for data in blenderModel:
                print(data)
                item = (dict(db.child('wixData').child(data).get().val()))
                if item.get('rendered'):
                    for elementItem in item.get('cizim'):
                        self.databaseItems.append(elementItem);

                    self.customerProperty.append({
                        'databaseId': item.get('wixId'),
                        'musteriAdi': item.get('musteriAdi'),
                        'musteriEmail': item.get('musteriEmail'),
                        'time': int(item.get('time')),
                        'databaseItems': self.databaseItems
                    })
        else:
            for data in blenderModel:
                item = dict(db.child('wixData').child(data).get().val())
                if not item.get('rendered'):
                    for elementItem in item.get('cizim'):
                        self.databaseItems.append(elementItem);

                    self.customerProperty.append({
                        'databaseId': data,
                        'musteriAdi': item.get('musteriAdi'),
                        'musteriEmail': item.get('musteriEmail'),
                        'time': int(item.get('time')),
                        'databaseItems': self.databaseItems
                    })

        """if self.filter == 'renderItem':
            for item in data:
                if item.get('rendered'):
                    self.databaseItems = []
                    for element in item['cizim']:
                        self.databaseItems.append(element);

                    self.customerProperty.append({
                        'databaseId': item.get('wixId'),
                        'musteriAdi': item.get('musteriAdi'),
                        'musteriEmail': item.get('musteriEmail'),
                        'time': int(item.get('time')),
                        'databaseItems': self.databaseItems
                    });"""

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
        db = self.firebase.database()

        db.child('wixData').child(id).update({"rendered": False})
        # requests.post('https://sarginapi.herokuapp.com/renders/update/' + id, {'renderedStatus': False})


if __name__ == '__main__':
    element = Collection();
    element.getDataFromDatabase()
