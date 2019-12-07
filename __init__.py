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
                 modul_genislik=0, locationX=0, locationY=0, locationZ=0, isim='Sargın', collection_adı='Yusuf',
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
    return obj


def collection_move(x, y, z, collection_adı):
    objects_sahne = bpy.data.collections[collection_adı].objects;

    for obj in objects_sahne:
        old_locationX, old_locationY, old_locationZ = obj.location;
        print(old_locationX)
        obj.location = (int(x + old_locationX), int(y + old_locationY), int(z + old_locationZ));


def kutu_Olustur():
    for key in DataCollection.data.keys():
        if type(DataCollection.data[key]) is dict:
            topOfItem = list(DataCollection.data[key].keys());
            if topOfItem[0] is 'dahil':
                new_Obj = Obje_Olsutur(kalinlik=DataCollection.data[key]['malzeme']['kalınlık'],
                                       derinlik=DataCollection.data[key]['en'],
                                       yukseklik=DataCollection.data[key]['boy'],
                                       modul_genislik=DataCollection.data[key]['en'],
                                       locationX=DataCollection.data[key]['x_1'],
                                       locationY=DataCollection.data[key]['y_1'],
                                       locationZ=DataCollection.data[key]['z_1'],
                                       yon=DataCollection.data[key].get('tip'),
                                       isim=DataCollection.data[key]['adı']);
            else:
                for data in list(DataCollection.data[key].keys()):
                    if list(DataCollection.data[key][data].values())[0] is True:
                        new_Obj2 = Obje_Olsutur(kalinlik=DataCollection.data[key][data]['malzeme']['kalınlık'],
                                                derinlik=DataCollection.data[key][data]['en'],
                                                yukseklik=DataCollection.data[key][data]['boy'],
                                                modul_genislik=DataCollection.data[key][data]['boy'],
                                                locationX=DataCollection.data[key][data].get('x_1'),
                                                locationY=DataCollection.data[key][data].get('y_1'),
                                                locationZ=DataCollection.data[key][data].get('z_1'),
                                                yon=DataCollection.data[key][data]['tip'],
                                                isim=DataCollection.data[key][data]['adı']);


if __name__ == '__main__':
    kutu_Olustur();
