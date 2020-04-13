import json
from random import randrange

import bpy

standard_kalinlik = 0.018;
standard_derinlik = 0.60;
standard_yukseklik = 0.75;
standard_genislik = 0.65;
sahnedeki_objeler = [];

config = {
    'isTest': False
}


class CreateObject:
    def __init__(self, data):
        self.lastData = []
        if config.get('isTest'):
            with open('../test.json', 'r', encoding='utf-8') as json_file:
                self.data = json.load(json_file)
            self.dataOrganize()
        else:
            self.data = data
            self.sahnedeki_objeler = []
            self.wall2 = []
            self.wall1 = []
            self.createdData = {}

    def collection_move(self, x, y, z, collection_adi):
        objects_sahne = bpy.data.collections[collection_adi].objects;

        for obj in objects_sahne:
            old_locationX, old_locationY, old_locationZ = obj.location;
            obj.location = (float(old_locationX - z), float(old_locationY - x), float(old_locationZ - y));

    def createNewCollection(self, CollectionName='Yusuf'):
        collection = bpy.data.collections.new(str(CollectionName));
        bpy.context.scene.collection.children.link(collection);
        return bpy.data.collections[CollectionName];

    def assignMaterial(self, textureAdi='test', obj=[]):
        obj.data.materials.append(bpy.data.materials[textureAdi])

    def Obje_Olsutur(self, kalinlik=standard_kalinlik, derinlik=standard_derinlik, yukseklik=standard_yukseklik,
                     modul_genislik=0, locationX=0, locationY=0, locationZ=0, isim='Sargın',
                     collection=[],
                     yon=1, texture='wood', wallType=0):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False)
        obj = bpy.context.scene.objects["Cube"]  # Get the object
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.context.view_layer.objects.active = obj
        obj.name = str(isim + '_' + str(yon) + '_' + str(len(self.lastData)) + '_' + str(wallType))

        if yon == 2:  # sağ_yan
            obj.dimensions = (derinlik, kalinlik, yukseklik)
            obj.location = (-(derinlik / 2), -(kalinlik / 2), -(yukseklik / 2))
        elif yon == 3:  # ust
            obj.dimensions = (derinlik, modul_genislik, kalinlik)
            obj.location = ((-derinlik / 2), (-modul_genislik / 2), (-kalinlik / 2))
        elif (yon == 1) or (yon == 4):  # kapak
            obj.dimensions = (kalinlik, modul_genislik, yukseklik)
            obj.location = (-(kalinlik / 2), -(modul_genislik / 2), -(yukseklik / 2))
        else:
            print('\n')

        if (locationX != 0) or (locationY != 0) or (locationZ != 0):
            x, y, z = obj.location

            obj.location = ((x - locationZ), (y - locationX), (z - locationY));

        self.sahnedeki_objeler.append(obj)
        collection.objects.link(obj)

        if int(wallType) == 1:
            self.wall2.append(obj)
        elif int(wallType) == 0:
            self.wall1.append(obj)

        return obj

    def controlTextureObj(self, controlData, obj):
        if 'tezgah' in controlData.get('isim', ''):
            self.assignMaterial('mermerBeyaz', obj)
        else:
            self.assignMaterial('wood', obj)

        return {'status': 'FINISH'}

    def calculateDraw(self, value, collection, wallType):
        for keyForSub, valueForSub in value.items():
            if type(valueForSub) == dict and valueForSub.get(
                    'dahil'):
                if 'kulp' in valueForSub.get('ad', ''):
                    # Kulplar için
                    """
                    Burada sadece kulplar var.
                    Burdan değerler alınıp çizilecek
                    """
                    self.createdData = {}
                else:
                    # Üst ve Alt Dolaplar için çizim
                    """
                        Burada sadece tip 3 yani üst,alt ve yatay raflar var.
                        Burdan değerler alınıp çizilecek

                        ********************
                        *                  *
                        ********************
                    """

                    if 'kapak2' in valueForSub.get('adı', ''):
                        print('KAPAK2******** RAF')

                    if value.get('cekmeceControl', False):
                        en = float(valueForSub.get('boy', 0))
                        boy = float(valueForSub.get('en', 0))
                    else:
                        en = float(valueForSub.get('en', 0))
                        boy = float(valueForSub.get('boy', 0))

                    self.createdData = {
                        'kalinlik': float(valueForSub.get('malzeme', {"mn": 0,
                                                                      "kn": 0,
                                                                      "adı": "66_Kar Beyaz",
                                                                      "kalınlık": 1.8,
                                                                      "image": "rgb(255,255,255)"}).get(
                            'kalınlık', 1.8)),
                        'derinlik': float(en),
                        'yukseklik': float(boy),
                        'modul_genislik': float(boy),
                        'locationX': float(valueForSub.get('x_1', 0)),
                        'locationY': float(valueForSub.get('y_1', 0)),
                        'locationZ': float(valueForSub.get('z_1', 0)),
                        'yon': int(valueForSub.get('tip', 3)),
                        'isim': valueForSub.get('adı', 'isimsiz'),
                        'collection': collection,
                        'wallType': wallType
                    }

        if value.get('dahil', False) and (value.get('tip', 0) == 1 or value.get('tip', 0) == 4):
            """
                Burada sadece tip 1 yani kapak,baza ve arkalık var. Bunlar dikey ürünler
                Burdan değerler alınıp çizilecek

                ***************
                *             *  
                *             * 
                *             *  
                *             *  
                ***************
            """
            if value.get('cekmeceControl', False) and ('kapak' not in value.get('adı', '')):
                en = float(value.get('boy', 0))
                boy = float(value.get('en', 0))
            else:
                en = float(value.get('en', 0))
                boy = float(value.get('boy', 0))

            if value.get('tip', 1) == 3:
                genislik = boy
            else:
                genislik = en

            """
            TODO:
                Sorun burda birden fazla ürün çiziyor.
            """
            # self.createdData = {
            #     'kalinlik': float(value.get('malzeme', {"mn": 0,
            #                                             "kn": 0,
            #                                             "adı": "66_Kar Beyaz",
            #                                             "kalınlık": 1.8,
            #                                             "image": "rgb(255,255,255)"}).get(
            #         'kalınlık', 1.8)),
            #     'derinlik': float(en),
            #     'yukseklik': float(boy),
            #     'modul_genislik': float(genislik),
            #     'locationX': float(value.get('x_1', 0)),
            #     'locationY': float(value.get('y_1', 0)),
            #     'locationZ': float(value.get('z_1', 0)),
            #     'yon': int(value.get('tip', 3)),
            #     'isim': value.get('adı', 'isimsiz'),
            #     'collection': collection,
            #     'wallType': wallType
            # }

            if ('baza' in value.get('adı', '')) or ('arka kuşak' in value.get('adı', '')):
                # print(key, value)
                self.createdData = {
                    'kalinlik': float(value.get('malzeme', {"mn": 0,
                                                            "kn": 0,
                                                            "adı": "66_Kar Beyaz",
                                                            "kalınlık": 1.8,
                                                            "image": "rgb(255,255,255)"}).get(
                        'kalınlık', 1.8)),
                    'derinlik': float(boy),
                    'yukseklik': float(en),
                    'modul_genislik': float(boy),
                    'locationX': float(value.get('x_1', 0)),
                    'locationY': float(value.get('y_1', 0)),
                    'locationZ': float(value.get('z_1', 0)),
                    'yon': int(value.get('tip', 3)),
                    'isim': value.get('adı', 'isimsiz'),
                    'collection': collection,
                    'wallType': wallType
                }

        elif value.get('dahil', False) and value.get('tip', 0) == 2:
            """
            Burada sadece tip 2 yani sağyan,solyan var. Bunlar dikey ürünler
            Burdan değerler alınıp çizilecek
            ***
            * *
            * *
            * *
            * *
            * *
            * *
            ***
            """
            if value.get('cekmeceControl', False):
                en = float(value.get('boy', 0))
                boy = float(value.get('en', 0))
            else:
                en = float(value.get('en', 0))
                boy = float(value.get('boy', 0))

            if 'kapak2' in value.get('adı', ''):
                print('KAPAK2******** SAĞ SOL YAN')

            self.createdData = {
                'kalinlik': float(value.get('malzeme', {"mn": 0,
                                                        "kn": 0,
                                                        "adı": "66_Kar Beyaz",
                                                        "kalınlık": 1.8,
                                                        "image": "rgb(255,255,255)"}).get(
                    'kalınlık', 1.8)),
                'derinlik': float(en),
                'yukseklik': float(boy),
                'modul_genislik': float(boy),
                'locationX': float(value.get('x_1', 0)),
                'locationY': float(value.get('y_1', 0)),
                'locationZ': float(value.get('z_1', 0)),
                'yon': int(value.get('tip', 3)),
                'isim': value.get('adı', 'isimsiz'),
                'collection': collection,
                'wallType': wallType
            }

        if len(self.createdData) != 0:
            try:
                addedObj = (self.Obje_Olsutur(
                    kalinlik=self.createdData.get('kalinlik', 1.8),
                    derinlik=self.createdData.get('derinlik', 0),
                    yukseklik=self.createdData.get('yukseklik', 0),
                    modul_genislik=self.createdData.get('modul_genislik', 0),
                    locationX=self.createdData.get('locationX', 0),
                    locationY=self.createdData.get('locationY', 0),
                    locationZ=self.createdData.get('locationZ', 0),
                    yon=self.createdData.get('yon', 0),
                    isim=self.createdData.get('isim', 0),
                    collection=self.createdData.get('collection', []),
                    wallType=self.createdData.get('wallType', 0)))
                # Append ListData
                self.lastData.append(addedObj)
                # Control Texture Element
                self.controlTextureObj(self.createdData, addedObj)
            except NameError:
                print(NameError)
            except ValueError:
                print(ValueError)

        return self.lastData

    def dataOrganize(self):
        modulNames: list = [];
        for items in self.data:
            collectionName: str = str(items.get('modül_adı', 'isimsiz')) + str(randrange(100))
            modulNames.append((collectionName, str(items.get('modül_adı', 'isimsiz'))));
            collection = self.createNewCollection(collectionName)
            wallType = items.get('duvar_no', 0)

            for key, value in items.items():
                if type(value) == dict:
                    self.calculateDraw(value, collection, wallType)
                elif type(value) == list and ('çk' in key):
                    for element in value:
                        if type(element) == dict:
                            for keyDict, valDict in element.items():
                                if type(valDict) == dict:
                                    valDict['cekmeceControl'] = True
                                    self.calculateDraw(valDict, collection, wallType)

            self.collection_move(items.get('x1'), items.get('y1'),
                                 items.get('z1'),
                                 collectionName)

        print('DATA Modül NAMEs \n')
        print(modulNames)
        print(len([item for item in modulNames if 'buzdolab' in item[0]]))
        print(len([item for item in self.data if 'buzdolab' in item.get('modül_adı', '')]))


if __name__ == '__main__':
    test = CreateObject()
