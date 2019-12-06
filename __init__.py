import bpy
import mathutils

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
    obj.name = str(str(len(sahnedeki_objeler)) + '_solyan_' + isim);

    if yon is 1:
        obj.dimensions = (derinlik, kalinlik, yukseklik);
        obj.location = (-(derinlik / 2), -(kalinlik / 2), (-yukseklik / 2));
    elif yon is 2:
        obj.dimensions = (derinlik, modul_genislik, kalinlik);
        obj.location = (-(derinlik / 2), -(modul_genislik / 2), (-kalinlik / 2));
    elif yon is 3:
        obj.dimensions = (kalinlik, modul_genislik, yukseklik);
        obj.location = (-(kalinlik / 2), -(modul_genislik / 2), -(yukseklik / 2));

    if (locationX is not 0) or (locationY is not 0) or (locationZ is not 0):
        x, y, z = obj.location;
        obj.location = ((x + locationX), (y + locationY), (z + locationZ));

    sahnedeki_objeler.append(obj);
    return obj


def collection_move(x, y, z, collection_adı):
    objects_sahne = bpy.data.collections[collection_adı].objects;

    for obj in objects_sahne:
        old_locationX, old_locationY, old_locationZ = obj.location;
        print(old_locationX)
        obj.location = (int(x + old_locationX), int(y + old_locationY), int(z + old_locationZ));


def kutu_Olustur():
    sol_yan = Obje_Olsutur(kalinlik=1.8, derinlik=45, yukseklik=75, yon=1);
    sag_yan = Obje_Olsutur(kalinlik=1.8, derinlik=45, yukseklik=75, locationY=-60, yon=1);
    ust_tabla = Obje_Olsutur(kalinlik=1.8, derinlik=45, modul_genislik=(60 - 1.8), locationY=-1.8, yon=2);
    alt_tabla = Obje_Olsutur(kalinlik=1.8, derinlik=45, modul_genislik=60, locationZ=-65, locationY=-(0.9), yon=2);
    arkalik = Obje_Olsutur(kalinlik=0.8, yukseklik=75, modul_genislik=60, yon=3);
    on_Kapak = Obje_Olsutur(kalinlik=1.8, yukseklik=65, modul_genislik=60, yon=3, locationX=-45, locationY=-0.9);


if __name__ == '__main__':
    kutu_Olustur();
