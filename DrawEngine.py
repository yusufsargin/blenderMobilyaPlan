import json


class CreateObject:
    def __init__(self):
        # self.data = db
        with open('test.json', 'r') as json_file:
            self.data = json.load(json_file)
        self.dataOrganize()


    def dataOrganize(self):
        self.lastData = []
        for items in self.data.get('cizim'):
            for key,value in items.items():
                if type(value) == dict:
                    print(value.items()['adı'])


if __name__ == '__main__':
    test = CreateObject()
