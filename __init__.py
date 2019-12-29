import bpy
import mathutils
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
                 collection=[],
                 yon=1, texture='test'):
    bpy.ops.mesh.primitive_cube_add(size=2);
    obj = bpy.context.active_object;
    obj.name = str(isim + '_' + str(yon));
    assignMaterial('wood', obj);

    if yon is 2:  # sağ_yan
        obj.dimensions = (derinlik, kalinlik, yukseklik);
        obj.location = (-(derinlik / 2), -(kalinlik / 2), (-yukseklik / 2));
    elif yon is 3:  # ust
        obj.dimensions = (derinlik, modul_genislik, kalinlik);
        obj.location = (-(derinlik / 2), -(modul_genislik / 2), (-kalinlik / 2));
    elif (yon is 1) or (yon is 4):  # kapak
        obj.dimensions = (kalinlik, modul_genislik, yukseklik);
        obj.location = (-(kalinlik / 2), -(modul_genislik / 2), -(yukseklik / 2));
    else:
        print(yon);
        print('\n');

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
            if DataCollectionJson[key].get('dahil', False) == True:
                # normal sol-sag-raf cizimler
                for dataName in topOfItem:
                    if type(DataCollectionJson[key][dataName]) is dict:
                        if dataName == 'malzeme':
                            # baza ve arka kuşak için çizim
                            if ('baza' in DataCollectionJson[key].get('adı', 'HATA') or 'arka kuşak' in
                                    DataCollectionJson[key].get('adı', 'HATA')):
                                Obje_Olsutur(kalinlik=DataCollectionJson[key][dataName].get('kalınlık', 1.8),
                                             derinlik=DataCollectionJson[key]['boy'],
                                             yukseklik=DataCollectionJson[key].get('en', 0),
                                             modul_genislik=DataCollectionJson[key].get('boy', 0),
                                             locationX=DataCollectionJson[key]['x_1'],
                                             locationY=DataCollectionJson[key]['y_1'],
                                             locationZ=DataCollectionJson[key]['z_1'],
                                             yon=DataCollectionJson[key].get('tip', 1),
                                             isim=DataCollectionJson[key]['adı'], collection=collection);
                            else:
                                '''
                                    Raf için genilik yer değiştirilmesi gerekiyor. Değişim yapıldı +1
                                    - Buzdolabı sabit raf z değeri yanlış
                                    - Kapak modülünde hatalar var
                                '''
                                if DataCollectionJson[key].get('tip') == 3:
                                    genislik = DataCollectionJson[key].get('boy');
                                else:
                                    genislik = DataCollectionJson[key].get('en');

                                Obje_Olsutur(kalinlik=DataCollectionJson[key][dataName].get('kalınlık', 1.8),
                                             derinlik=DataCollectionJson[key]['en'],
                                             yukseklik=DataCollectionJson[key].get('boy', 0),
                                             modul_genislik=genislik,
                                             locationX=DataCollectionJson[key]['x_1'],
                                             locationY=DataCollectionJson[key]['y_1'],
                                             locationZ=DataCollectionJson[key]['z_1'],
                                             yon=DataCollectionJson[key].get('tip', 1),
                                             isim=DataCollectionJson[key]['adı'], collection=collection);

            # Üst Ve Alt çizimi için
            else:
                # üst çizim
                for dataDict in topOfItem:
                    if type(DataCollectionJson[key][dataDict]) is dict and type(
                            DataCollectionJson[key][dataDict]) is not int:
                        if DataCollectionJson[key][dataDict].get('dahil', False) is True:
                            if (dataDict != 'kulp'):
                                Obje_Olsutur(
                                    kalinlik=DataCollectionJson[key][dataDict].get('malzeme', {"mn": 0,
                                                                                               "kn": 0,
                                                                                               "adı": "66_Kar Beyaz",
                                                                                               "kalınlık": 1.8,
                                                                                               "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8),
                                    derinlik=DataCollectionJson[key][dataDict]['en'],
                                    yukseklik=DataCollectionJson[key][dataDict]['boy'],
                                    modul_genislik=DataCollectionJson[key][dataDict]['boy'],
                                    locationX=DataCollectionJson[key][dataDict]['x_1'],
                                    locationY=DataCollectionJson[key][dataDict]['y_1'],
                                    locationZ=DataCollectionJson[key][dataDict]['z_1'],
                                    yon=DataCollectionJson[key][dataDict].get('tip', 3),
                                    isim=DataCollectionJson[key][dataDict]['adı'],
                                    collection=collection);

        elif (type(DataCollectionJson[key]) is list):
            for element in DataCollectionJson[key]:
                if type(element) is dict:
                    for keyData in element.keys():
                        if type(element[keyData]) is dict:
                            if element[keyData].get('dahil', False) == True:
                                # Kapak  çizim
                                if 'kapak' in keyData:
                                    Obje_Olsutur(kalinlik=element[keyData].get('malzeme', {"mn": 0,
                                                                                           "kn": 0,
                                                                                           "adı": "66_Kar Beyaz",
                                                                                           "kalınlık": 1.8,
                                                                                           "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8),
                                        derinlik=element[keyData].get('en', 0),
                                        yukseklik=element[keyData].get('boy'),
                                        modul_genislik=element[keyData].get('en', 0),
                                        locationX=element[keyData].get('x_1', 50),
                                        locationY=element[keyData].get('y_1', 0),
                                        locationZ=element[keyData].get('z_1', 0),
                                        yon=element[keyData].get('tip', 2),
                                        isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                        collection=collection);
                                elif element[keyData].get('tip', 2) == 1:
                                    Obje_Olsutur(kalinlik=element[keyData].get('malzeme', {"mn": 0,
                                                                                           "kn": 0,
                                                                                           "adı": "66_Kar Beyaz",
                                                                                           "kalınlık": 1.8,
                                                                                           "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8),
                                        derinlik=element[keyData].get('en', 0),
                                        yukseklik=element[keyData].get('en'),
                                        modul_genislik=element[keyData].get('boy', 0),
                                        locationX=element[keyData].get('x_1', 50),
                                        locationY=element[keyData].get('y_1', 0),
                                        locationZ=element[keyData].get('z_1', 0),
                                        yon=element[keyData].get('tip', 2),
                                        isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                        collection=collection);
                                elif element[keyData].get('tip', 2) == 2:
                                    Obje_Olsutur(kalinlik=element[keyData].get('malzeme', {"mn": 0,
                                                                                           "kn": 0,
                                                                                           "adı": "66_Kar Beyaz",
                                                                                           "kalınlık": 1.8,
                                                                                           "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8),
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
                                    Obje_Olsutur(kalinlik=element[keyData].get('maleme', {"mn": 0,
                                                                                          "kn": 0,
                                                                                          "adı": "66_Kar Beyaz",
                                                                                          "kalınlık": 1.8,
                                                                                          "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8),
                                        derinlik=element[keyData].get('en', 0),
                                        yukseklik=element[keyData].get('boy'),
                                        modul_genislik=element[keyData].get('en', 0),
                                        locationX=element[keyData].get('x_1', 50),
                                        locationY=element[keyData].get('y_1', 0),
                                        locationZ=element[keyData].get('z_1', 0),
                                        yon=element[keyData].get('tip', 2),
                                        isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                        collection=collection);


def kameraOlustur():
    bpy.ops.object.camera_add(enter_editmode=False, location=mathutils.Vector((-600.0, -180.0, -160.0)));
    bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='GLOBAL',
                             orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                             constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
                             proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                             use_proportional_projected=False);
    bpy.ops.transform.rotate(value=-1.5708, orient_axis='Y', orient_type='GLOBAL',
                             orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                             constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
                             proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                             use_proportional_projected=False);
    bpy.context.object.data.sensor_width = 50;


def renderAl(customerEmail, id):
    scene = bpy.context.scene;
    scene.render.image_settings.file_format = 'PNG';
    scene.render.filepath = 'D:\\blenderRenderImage\\' + customerEmail + '_' + id + '.png';
    data = bpy.ops.render.render('INVOKE_DEFAULT', write_still=True);
    print(data);


def assignMaterial(textureAdı='test', obj=bpy.context.active_object):
    obj.data.materials.append(bpy.data.materials[textureAdı]);


if __name__ == '__main__':
    databaseItem = DatabaseConnection.Collection();
    databaseItem.getDataFromDatabase();
    mod_isim = [];
    count = 0;

    for element in databaseItem.databaseItems:
        mod_isim.append(element['modül_adı']);
        ad = element['modül_adı'];

        for isim in mod_isim:
            if ad == isim:
                ad = str(element['modül_adı']) + '_' + str(count);
                count = count + 1;
        print(ad);
        kutu_Olustur(element, ad);
        collection_move(element['x1'], element['y1'],
                        element['z1'],
                        ad);

    kameraOlustur();
    renderAl('yusufsargin9@gmail.com', '123');
