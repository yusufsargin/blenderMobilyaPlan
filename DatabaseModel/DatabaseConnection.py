import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import db


class Collection:
    def __init__(self):
        self.databaseItems = []
        self.customerProperty = []
        self.filter = 'renderItem'
        self.renderedData = {}
        self.shortedData = []

        configForPyrebase = {
            "apiKey": "AIzaSyDN2GcZbIwk5wpW-7KkWYPRN_Yf1KBJnQk",
            "authDomain": "blender-44440.firebaseapp.com",
            "databaseURL": "https://blender-44440.firebaseio.com",
            "projectId": "blender-44440",
            "storageBucket": "blender-44440.appspot.com",
            "messagingSenderId": "625093549043",
            "appId": "1:625093549043:web:fb06aaeae958bd44a15086"
        }

        configForAdmin = {
            "type": "service_account",
            "project_id": "blender-44440",
            "private_key_id": "57327c81301517fe48038c14a3a0cdb3dd0f04cb",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDEeI2yOAmhHFW9\nS2dHJUiVhwtLsi5QvslkZ4gtx7S5lMfN/tschM0WxTM5K+nDl8uOxfkvMlI1Qcfb\nGpzF15ff6EoWCSNLLFuKfjvArhlP7vEkDr/2M606Hty24efyWdZlPDhq5aETQ6L9\nE3GyXQ+IywtLuYB4SK20oZrCZrac1hhTrYfSuMEtyd+NEH7jnjkyAKnAwvoqkefA\nJpqfGz86mBc52jPOhv2eDjMIo1QSs/viKJQRO7kP6GXCKgYuKxUw/izxNh3JrcKe\ngqsTZhyF0WnT2OQa033BISU3XhwkBGUOJwjdV/D1tgfkXk4ihSUq220tsEvKeP3R\n/TPHZJb3AgMBAAECggEABzs0rQ9LPJSs1OnIkg9dq42HUed9/lcb5+yTmUYMA4kv\nDXZa5n4+h+gp6XwRkdfSAguxWF+BD2Gbbs6hhIzsJfaaoAncokL3jUk/SFbyYY5b\nbg/kWJGeEL7bes8lfVsLtBTADkTjZYv55epoS5tSrgxjHwv11PeI/A0k8TVcmd1m\nOE6OiTDS1J5/JPMFVomFaf5TSU3q32jDdb0/TmSGuGOi70PIStfu6tFOzSe1ai7C\nFYbSiv6Hul1LUq7sT5c3XCBCGM5cysOlTnZMhdcIv43PvYEMerjdUCS+GunsS/6Z\nEy5RPtcdSCjv/Bl68LT44dhvbMcsdpRGjlu6l6V5uQKBgQD+VJEyTJBHm+wggOM1\ntxopfMquonpE+ZegoeHWgsDK3nzbzNBt6CxBq8JImHNeY66kVYblAz7uWEARS8xe\nazKgLqwjEjLoiWkCNjJyP0lYABs010ZHutDVqnf0i4/EKRq792FLCSdrwJS6gGPi\n1+A7MXouErJixKG84HTv/PGPJQKBgQDFwr8fl2tJ8kXmWBKKfZVlYC7i0tWhFT2X\n1F9uG6x3NDWQO+o9J0wJsK87o5NnROc0AtrVuHBtSfpLlIaq4DTVv3Qsasg2VEfW\nRh7vFYFFTSVWyxfZ0XESv33/z+b9KDIf4wAJixLOZIv6RZsn6OCxhG/NlazFb1io\nK7Tj1w5w6wKBgQDTlJTqTGmnOR76d18OG9Km+ws+tyqS4TV0S9gudb5fxzIGRWCM\nXp8azwIlFLa9qp3qVsCPGuEqtb4u5WkSj4mhWtKXppc1fsMeNOpIwz+H9yarEgCE\nwfTkHBoJFmW24h88inOlUes6qA7TDOaMG92OQP4NAD7pDf4jvHNsB3kKBQKBgFrl\nv4laxNKxTBWrB6KmRIPbKNHTDKREqhHeaJqol6YW1kPcdjbzmAygLHsiHX+K+SY7\n5a/0XaCuLyCMPTXPZhmVLWW5Ext9s6M2icNkxA1Bf1ccdHMGxI1UfSqWudpEnn1v\njjXUuakqJ/i6A63daWHOuMDq+gWpvztVE4jh8V5PAoGAEM64U+/8rnwa9sHziOxN\nwx11WXvzAzjfoQWkmm3/oEVA/I15r9URsNojUy55OzeVDN8RefTliJkicjH1Ac5q\ns9eevZ0V3aSDXciBRGaAvMYBniG9YBUR0PQOAZEDeTsq8ni2HFlTfdLIdORfNAZT\n4+QUmBJDMk6KKwc+XbQPHJI=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-fy3if@blender-44440.iam.gserviceaccount.com",
            "client_id": "114973086361338486647",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fy3if%40blender-44440.iam.gserviceaccount.com"
        }

        self.config = credentials.Certificate(configForAdmin)

        if (not len(firebase_admin._apps)):
            firebase_admin.initialize_app(self.config, {
                'databaseURL': 'https://blender-44440.firebaseio.com/'
            })

        self.firebase = pyrebase.initialize_app(configForPyrebase)
        self.database = db.reference('/wixData')

    def getDataFromDatabase(self):
        # data = json.loads(requests.get('https://sarginapi.herokuapp.com/renders').text);
        # db = self.firebase.database()

        blenderModel = self.database.get()

        if blenderModel is not None:
            if self.filter == 'renderItem':
                for data in blenderModel:
                    item = self.database.child(data).get()
                    if item.get('rendered') and item.get('cizim') != None:
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
                    item = self.database.child(data).get()
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
        self.database.child(id).update({"rendered": False})
        # requests.post('https://sarginapi.herokuapp.com/renders/update/' + id, {'renderedStatus': False})

    def appendErrorMessage(self, id, message='err'):
        errMessage = self.database.child(id).get()

        if errMessage.get('errors') is not None:
            errMessage.get('errors').append(message)
        else:
            errMessage.get('errors', []).append(message)

        self.database.child(id).update({'errors', errMessage})

        return True

    def saveImage(self, imgName, imgFilePath, id):
        storage = self.firebase.storage()

        storage.child('renders/' + imgName).put(imgFilePath, 'test')
        imgUrl = storage.child('renders/' + imgName).get_url('test')

        self.database.child(id).update({'imgUrl': imgUrl})

        return 'Finish'


if __name__ == '__main__':
    element = Collection()
