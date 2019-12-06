import bpy
import mathutils

standard_kalınlık = 0.018;
standard_deinlik = 0.60;
standard_yukseklik = 0.75;
standard_genislik = 0.65;
obj_sayı = 1;


def kasa_Olsutur(kalinlik, derinlik, yukseklik, modul_genislik, isim, collection_adı='Yusuf', yon=1):
    bpy.ops.mesh.primitive_cube_add(size=2);
    sol_yan = bpy.context.active_object;
    sol_yan.name = str(str(obj_sayı) + '_solyan_' + isim);
    if yon is 1:
        sol_yan.dimensions = (derinlik, kalinlik, yukseklik);
        sol_yan.location = (-(derinlik / 2), -(kalinlik / 2), (-yukseklik / 2));
    elif yon is 2:
        sol_yan.dimensions = (derinlik, modul_genislik, kalinlik);
        sol_yan.location = (-(derinlik / 2), -(modul_genislik / 2), (-kalinlik / 2));


def collection_move(x, y, z, collection_adı):
    objects_sahne = bpy.data.collections[collection_adı].objects;

    for obj in objects_sahne:
        old_locationX, old_locationY, old_locationZ = obj.location;
        print(old_locationX)
        obj.location = (int(x + old_locationX), int(y + old_locationY), int(z + old_locationZ));


if __name__ == '__main__':
    kasa_Olsutur(1.8, 65, 75, 70, 'Deneme1', yon=2);
    kasa_Olsutur(1.8, 65, 75, 70, 'Deneme1', yon=1);
    # collection_move(-9, -9, 65, 'Yusuf');
