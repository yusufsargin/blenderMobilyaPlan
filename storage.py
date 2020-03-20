import json
from random import randrange

import bpy

standard_kalinlik = 0.018;
standard_derinlik = 0.60;
standard_yukseklik = 0.75;
standard_genislik = 0.65;
sahnedeki_objeler = [];

config = {
    'isTest': True
}


class CreateObject:
    def __init__(self):
        with open('test.json', 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)

        self.dataOrganize()

    def collection_move(self, x, y, z, collection_adi):
        objects_sahne = bpy.data.collections[collection_adi].objects;

        for obj in objects_sahne:
            old_locationX, old_locationY, old_locationZ = obj.location;
            obj.location = (float(old_locationX - z), float(old_locationY - x), float(old_locationZ - y));

    def createNewCollection(self, CollectionName='Yusuf'):
        collection = bpy.data.collections.new(str(CollectionName));
        bpy.context.scene.collection.children.link(collection);
        return bpy.data.collections[CollectionName];

    def assignMaterial(self, textureAdi='test', obj=''):
        obj.data.materials.append(bpy.data.materials[textureAdi])

    def Obje_Olsutur(self, kalinlik=standard_kalinlik, derinlik=standard_derinlik, yukseklik=standard_yukseklik,
                     modul_genislik=0, locationX=0, locationY=0, locationZ=0, isim='Sargın',
                     collection=[],
                     yon=1, texture='wood', wallType='0'):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False)
        obj = bpy.context.scene.objects["Cube"]  # Get the object
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.context.view_layer.objects.active = obj
        obj.name = str(isim + '_' + str(yon) + '_' + str(randrange(100)) + '_' + str(wallType))
        self.assignMaterial(texture, obj)

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
                    pass
                else:
                    pass
                    # Üst ve Alt Dolaplar için çizim
                    """
                        Burada sadece tip 3 yani üst,alt ve yatay raflar var.
                        Burdan değerler alınıp çizilecek

                        ********************
                        *                  * 
                        ********************
                    """
                    self.lastData.append(self.Obje_Olsutur(
                        kalinlik=float(valueForSub.get('malzeme', {"mn": 0,
                                                                   "kn": 0,
                                                                   "adı": "66_Kar Beyaz",
                                                                   "kalınlık": 1.8,
                                                                   "image": "rgb(255,255,255)"}).get(
                            'kalınlık', 1.8)),
                        derinlik=float(valueForSub.get('en', 0)),
                        yukseklik=float(valueForSub.get('boy', 0)),
                        modul_genislik=float(valueForSub.get('boy', 0)),
                        locationX=float(valueForSub.get('x_1', 0)),
                        locationY=float(valueForSub.get('y_1', 0)),
                        locationZ=float(valueForSub.get('z_1', 0)),
                        yon=int(valueForSub.get('tip', 3)),
                        isim=valueForSub.get('adı', 'isimsiz'),
                        collection=collection, wallType=wallType))

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
            if ('baza' in value.get('adı')) or ('arka kuşak' in value.get('adı')):
                # print(key, value)
                self.lastData.append(self.Obje_Olsutur(
                    kalinlik=float(value.get('malzeme', {}).get('kalınlık', 1.8)),
                    derinlik=float(value.get('boy', 0)),
                    yukseklik=float(value.get('en', 0)),
                    modul_genislik=float(value.get('boy', 0)),
                    locationX=float(value.get('x_1', 0)),
                    locationY=float(value.get('y_1', 0)),
                    locationZ=float(value.get('z_1', 0)),
                    yon=int(value.get('tip', 1)),
                    isim=value.get('adı', 'ERR'), collection=collection,
                    wallType=wallType))
            else:
                if value.get('tip', 1) == 3:
                    genislik = value.get('boy', 0);
                else:
                    genislik = value.get('en', 0);

                self.lastData.append(self.Obje_Olsutur(
                    kalinlik=float(value.get('malzeme', {}).get('kalınlık', 1.8)),
                    derinlik=float(value.get('en', 0)),
                    yukseklik=float(value.get('boy', 0)),
                    modul_genislik=float(genislik),
                    locationX=float(value.get('x_1', 0)),
                    locationY=float(value.get('y_1', 0)),
                    locationZ=float(value.get('z_1', 0)),
                    yon=int(value.get('tip', 1)),
                    isim=value.get('adı', 'isimsiz'),
                    collection=collection, wallType=wallType))

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
            self.lastData.append(self.Obje_Olsutur(kalinlik=float(value.get('malzeme', {"mn": 0,
                                                                                        "kn": 0,
                                                                                        "adı": "66_Kar Beyaz",
                                                                                        "kalınlık": 1.8,
                                                                                        "image": "rgb(255,255,255)"}).get(
                'kalınlık', 1.8)),
                derinlik=float(value.get('en', 0)),
                yukseklik=float(value.get('boy')),
                modul_genislik=float(value.get('boy', 0)),
                locationX=float(value.get('x_1', 0)),
                locationY=float(value.get('y_1', 0)),
                locationZ=float(value.get('z_1', 0)),
                yon=int(value.get('tip', 2)),
                isim=value.get('adı', 'Hatalı_Control_Et'),
                collection=collection, wallType=wallType))

    def dataOrganize(self):
        self.lastData = []

        for items in self.data.get('wixData').get('7b5f59c1-66ca-4f79-a68d-bdd6f0c5ba9b').get('cizim'):
            collectionName = str(items.get('modül_adı', 'isimsiz')) + str(randrange(100))
            collection = self.createNewCollection(collectionName)
            wallType = items.get('duvar_no', 0)

            for key, value in items.items():
                if type(value) == list and ('çk' in key):
                    for element in value:
                        for keyDict, valDict in element.items():
                            if type(valDict) == dict:
                                self.calculateDraw(valDict, collection, wallType)


if __name__ == '__main__':
    test = CreateObject()
