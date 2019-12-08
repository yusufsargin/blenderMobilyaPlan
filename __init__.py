import bpy
import mathutils
import DataCollection

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
            obj.location = ((x - locationY), (y - locationX), (z - locationZ));

    sahnedeki_objeler.append(obj);
    bpy.ops.collection.objects_remove_all();
    collection.objects.link(obj);
    return obj


def collection_move(x, y, z, collection_adı):
    objects_sahne = bpy.data.collections[collection_adı].objects;

    for obj in objects_sahne:
        old_locationX, old_locationY, old_locationZ = obj.location;
        print(old_locationX)
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
                            obj = Obje_Olsutur(kalinlik=DataCollectionJson[key][dataName]['kalınlık'],
                                               derinlik=DataCollectionJson[key]['en'],
                                               yukseklik=DataCollectionJson[key]['boy'],
                                               modul_genislik=DataCollectionJson[key]['en'],
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


if __name__ == '__main__':
    kutu_Olustur(DataCollection.data, DataCollection.data['modül_adı']);
    collection_move(DataCollection.data['x1'], DataCollection.data['y1'], DataCollection.data['z1'],
                    DataCollection.data['modül_adı']);

    kutu_Olustur(DataCollection.altData, DataCollection.altData['modül_adı']);
    collection_move(DataCollection.altData['x1'], DataCollection.altData['y1'], DataCollection.altData['z1'],
                    DataCollection.altData['modül_adı']);
