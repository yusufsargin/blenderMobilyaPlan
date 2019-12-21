import bpy
import mathutils
import DataCollection
import DatabaseConnection

standard_kalinlik = 0.018;
standard_derinlik = 0.60;
standard_yukseklik = 0.75;
standard_genislik = 0.65;
obj_sayı = 1;
sahnedeki_objeler = [];


def make_offset(obj, yon=1, ust=0, yan=0):
    x, y, z = obj.dimensions;
    if ust is not 0:
        if yon is 1:
            obj.dimensions = (x, y, abs(z - (ust * 2)));
        elif yon is 2:
            obj.dimensions = (x, abs(y - (ust * 2)), z);
        elif yon is 3:
            obj.dimensions = (x, y, abs(z - (ust * 2)));
    elif yan is not 0:
        if yon is 1:
            obj.dimensions = (abs(x - (yan * 2)), y, z);
        elif yon is 2:
            obj.dimensions = (abs(x - (yan * 2)), y, z);
        elif yon is 3:
            obj.dimensions = (x, abs(y - (yan * 2)), z);


def Obje_Olsutur(kalinlik=standard_kalinlik, derinlik=standard_derinlik, yukseklik=standard_yukseklik,
                 modul_genislik=0, locationX=0, locationY=0, locationZ=0, isim='Sargın',
                 collection=bpy.data.collections[0],
                 yon=1):
    bpy.ops.mesh.primitive_cube_add(size=2);
    obj = bpy.context.active_object;
    obj.name = str(isim + '_' + str(yon));

    if yon is 2:  # sağ_yan
        obj.dimensions = (derinlik, kalinlik, yukseklik);
        obj.location = (-(derinlik / 2), -(kalinlik / 2), (-yukseklik / 2));
    elif yon is 3:  # ust
        obj.dimensions = (derinlik, modul_genislik, kalinlik);
        obj.location = (-(derinlik / 2), -(modul_genislik / 2), (-kalinlik / 2));
    elif yon is 1:  # kapak
        obj.dimensions = (kalinlik, modul_genislik, yukseklik);
        obj.location = (-(kalinlik / 2), -(modul_genislik / 2), -(yukseklik / 2));
    elif yon is None:
        return 'Not'

    if (locationX is not 0) or (locationY is not 0) or (locationZ is not 0):
        x, y, z = obj.location;
        if yon is 1:
            obj.location = ((x - locationZ), (y - locationX), (z - locationY));
        elif yon is 3:
            obj.location = ((x - locationZ), (y - locationX), (z - locationY));
        else:
            obj.location = ((x - locationZ), (y - locationX), (z - locationY));

    sahnedeki_objeler.append(obj);
    bpy.ops.collection.objects_remove_all();
    collection.objects.link(obj);
    return obj


def collection_move(x, y, z, collection_adı):
    objects_sahne = bpy.data.collections[collection_adı].objects;

    for obj in objects_sahne:
        old_locationX, old_locationY, old_locationZ = obj.location;
        obj.location = (int(old_locationX - z), int(old_locationY - x), int(old_locationZ - y));


def createNewCollection(CollectionName='Yusuf'):
    collection = bpy.data.collections.new(str(CollectionName));
    bpy.context.scene.collection.children.link(collection);
    return bpy.data.collections[CollectionName];


def kutu_Olustur(DataCollectionJson, CollectionName='Yusuf'):
    collection = createNewCollection(CollectionName);

    for key in DataCollectionJson.keys():
        if type(DataCollectionJson[key]) is dict:
            topOfItem = list(DataCollectionJson[key].keys());
            if (topOfItem[0] is 'dahil') and (DataCollectionJson[key][topOfItem[0]] is True):
                for dataName in topOfItem:
                    if type(DataCollectionJson[key][dataName]) is dict:
                        if dataName is 'malzeme':
                            if 'baza' in DataCollectionJson[key].get('adı', 'HATA'):
                                Obje_Olsutur(kalinlik=DataCollectionJson[key][dataName].get('kalınlık', 0),
                                             derinlik=DataCollectionJson[key]['boy'],
                                             yukseklik=DataCollectionJson[key].get('en', 0),
                                             modul_genislik=DataCollectionJson[key].get('boy', 0),
                                             locationX=DataCollectionJson[key]['x_1'],
                                             locationY=DataCollectionJson[key]['y_1'],
                                             locationZ=DataCollectionJson[key]['z_1'],
                                             yon=DataCollectionJson[key].get('tip'),
                                             isim=DataCollectionJson[key]['adı'], collection=collection);
                            else:
                                Obje_Olsutur(kalinlik=DataCollectionJson[key][dataName]['kalınlık'],
                                             derinlik=DataCollectionJson[key]['en'],
                                             yukseklik=DataCollectionJson[key].get('boy', 0),
                                             modul_genislik=DataCollectionJson[key].get('en', 0),
                                             locationX=DataCollectionJson[key]['x_1'],
                                             locationY=DataCollectionJson[key]['y_1'],
                                             locationZ=DataCollectionJson[key]['z_1'],
                                             yon=DataCollectionJson[key].get('tip'),
                                             isim=DataCollectionJson[key]['adı'], collection=collection);
                        else:
                            if DataCollectionJson[key][dataName]['dahil'] is True and dataName is not 'kulp':
                                obj = Obje_Olsutur(kalinlik=DataCollectionJson[key][dataName]['malzeme']['kalınlık'],
                                                   derinlik=DataCollectionJson[key][dataName]['en'],
                                                   yukseklik=DataCollectionJson[key][dataName]['boy'],
                                                   modul_genislik=DataCollectionJson[key][dataName]['en'],
                                                   locationX=DataCollectionJson[key][dataName]['x_1'],
                                                   locationY=DataCollectionJson[key][dataName]['y_1'],
                                                   locationZ=DataCollectionJson[key][dataName]['z_1'],
                                                   yon=DataCollectionJson[key][dataName]['tip'],
                                                   isim=DataCollectionJson[key][dataName]['adı'],
                                                   collection=collection);

            else:
                for dataDict in topOfItem:
                    if type(DataCollectionJson[key][dataDict]) is dict and type(
                            DataCollectionJson[key][dataDict]) is not int:
                        if 'dahil' in DataCollectionJson[key][dataDict]:
                            if DataCollectionJson[key][dataDict]['dahil'] is True:
                                obj = Obje_Olsutur(kalinlik=DataCollectionJson[key][dataDict]['malzeme']['kalınlık'],
                                                   derinlik=DataCollectionJson[key][dataDict]['en'],
                                                   yukseklik=DataCollectionJson[key][dataDict]['boy'],
                                                   modul_genislik=DataCollectionJson[key][dataDict]['en'],
                                                   locationX=DataCollectionJson[key][dataDict]['x_1'],
                                                   locationY=DataCollectionJson[key][dataDict]['y_1'],
                                                   locationZ=DataCollectionJson[key][dataDict]['z_1'],
                                                   yon=DataCollectionJson[key][dataDict]['tip'],
                                                   isim=DataCollectionJson[key][dataDict]['adı'],
                                                   collection=collection);

        elif (type(DataCollectionJson[key]) is list):
            for element in DataCollectionJson[key]:
                if type(element) is dict:
                    for keyData in element.keys():
                        if type(element[keyData]) is dict:
                            if element[keyData]['dahil'] is True:
                                if keyData is 'kapak':
                                    Obje_Olsutur(kalinlik=element[keyData]['malzeme'].get('kalınlık', 1.8),
                                                 derinlik=element[keyData].get('en', 0),
                                                 yukseklik=element[keyData].get('boy'),
                                                 modul_genislik=element[keyData].get('en', 0),
                                                 locationX=element[keyData].get('x_1', 50),
                                                 locationY=element[keyData].get('y_1', 0),
                                                 locationZ=element[keyData].get('z_1', 0),
                                                 yon=element[keyData].get('tip', 2),
                                                 isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                                 collection=collection);
                                elif element[keyData].get('tip') is 1:
                                    Obje_Olsutur(kalinlik=element[keyData]['malzeme'].get('kalınlık', 1.8),
                                                 derinlik=element[keyData].get('en', 0),
                                                 yukseklik=element[keyData].get('en'),
                                                 modul_genislik=element[keyData].get('boy', 0),
                                                 locationX=element[keyData].get('x_1', 50),
                                                 locationY=element[keyData].get('y_1', 0),
                                                 locationZ=element[keyData].get('z_1', 0),
                                                 yon=element[keyData].get('tip', 2),
                                                 isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                                 collection=collection);
                                elif element[keyData].get('tip') is 2:
                                    Obje_Olsutur(kalinlik=element[keyData]['malzeme'].get('kalınlık', 1.8),
                                                 derinlik=element[keyData].get('boy', 0),
                                                 yukseklik=element[keyData].get('en'),
                                                 modul_genislik=element[keyData].get('boy', 0),
                                                 locationX=element[keyData].get('x_1', 50),
                                                 locationY=element[keyData].get('y_1', 0),
                                                 locationZ=element[keyData].get('z_1', 0),
                                                 yon=element[keyData].get('tip', 2),
                                                 isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                                 collection=collection);
                                else:
                                    Obje_Olsutur(kalinlik=element[keyData]['malzeme'].get('kalınlık', 1.8),
                                                 derinlik=element[keyData].get('en', 0),
                                                 yukseklik=element[keyData].get('boy'),
                                                 modul_genislik=element[keyData].get('en', 0),
                                                 locationX=element[keyData].get('x_1', 50),
                                                 locationY=element[keyData].get('y_1', 0),
                                                 locationZ=element[keyData].get('z_1', 0),
                                                 yon=element[keyData].get('tip', 2),
                                                 isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                                 collection=collection);


if __name__ == '__main__':
    """ kutu_Olustur(DataCollection.data, DataCollection.data['modül_adı']);
     collection_move(DataCollection.data['x1'], DataCollection.data['y1'], DataCollection.data['z1'],
                     DataCollection.data['modül_adı']);
 
     kutu_Olustur(DataCollection.altData, DataCollection.altData['modül_adı']);
     collection_move(DataCollection.altData['x1'], DataCollection.altData['y1'], DataCollection.altData['z1'],
                     DataCollection.altData['modül_adı']);"""

    databaseItem = DatabaseConnection.Collection();
    databaseItem.getDataFromDatabase()

    for element in databaseItem.databaseItems:
        kutu_Olustur(element, element['modül_adı']);
        collection_move(element['x1'], element['y_1'], element['z_1'], element['modül_adı']);

""" kutu_Olustur(DataCollection.boy_dolap, DataCollection.boy_dolap['modül_adı']);
 collection_move(DataCollection.boy_dolap['x1'], DataCollection.boy_dolap['y1'],
                 DataCollection.boy_dolap['z1'],
                 DataCollection.boy_dolap['modül_adı']);

 kutu_Olustur(DataCollection.cekmeceli_dolap_1, DataCollection.cekmeceli_dolap_1['modül_adı']);
 collection_move(DataCollection.cekmeceli_dolap_1['x1'], DataCollection.cekmeceli_dolap_1['y1'],
                 DataCollection.cekmeceli_dolap_1['z1'],
                 DataCollection.cekmeceli_dolap_1['modül_adı']);

 kutu_Olustur(DataCollection.cekmeceli_dolap_2, DataCollection.cekmeceli_dolap_2['modül_adı']);
 collection_move(DataCollection.cekmeceli_dolap_2['x1'], DataCollection.cekmeceli_dolap_2['y1'],
                 DataCollection.cekmeceli_dolap_2['z1'],
                 DataCollection.cekmeceli_dolap_2['modül_adı']);
"""
