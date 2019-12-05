import bpy
import mathutils

standard_kalınlık = 0.018;
standard_deinlik = 0.60;
standard_yukseklik = 0.75;
standard_genislik = 0.65;
obj_sayı = 1;


def kasaOlsutur(kalinlik, derinlik, yukseklik, modul_genislik, isim, collection_adı='Yusuf', yon=1):
    bpy.ops.mesh.primitive_cube_add(size=2);
    sol_yan = bpy.context.active_object;
    sol_yan.name = str(str(obj_sayı) + '_solyan_' + isim);
    if yon is 1:
        sol_yan.dimensions = (derinlik, kalinlik, yukseklik);
    elif yon is 2:
        sol_yan.dimensions = (derinlik, modul_genislik, kalinlik);


def collection_move(x, y, z, collection_adı):
    objects_sahne = bpy.data.collections[collection_adı].objects;

    for obj in objects_sahne:
        obj.location = (x, y, z);


def cursor_koseye_sıfırlama():
    bpy.ops.object.mode_set(mode='OBJECT');
    obj = bpy.context.active_object;
    bpy.ops.object.mode_set(mode='EDIT');
    bpy.ops.mesh.select_mode(type='VERT');
    bpy.ops.mesh.select_all(action='DESELECT');



if __name__ == '__main__':
    kasaOlsutur(1.8, 65, 75, 70, 'Deneme1', yon=1);
    kasaOlsutur(1.8, 65, 75, 70, 'Deneme1', yon=2);
    collection_move(1, 5, 2, 'Yusuf')
