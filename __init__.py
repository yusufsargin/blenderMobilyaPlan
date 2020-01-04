import bpy
import mathutils
import DatabaseConnection
from bpy.app.handlers import persistent
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import threading
from functools import wraps
import mathutils
import math

standard_kalinlik = 0.018;
standard_derinlik = 0.60;
standard_yukseklik = 0.75;
standard_genislik = 0.65;
sahnedeki_objeler = [];

global CustomerEmail
global CustomerName

bl_info = {
    "name": "Sargin Render",
    "author": "Yusuf Sargin",
    "version": (0, 5, 6, 6),
    "blender": (2, 8, 0)
}


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
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False);
    obj = bpy.context.scene.objects["Cube"]  # Get the object
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    bpy.context.view_layer.objects.active = obj
    obj.name = str(isim + '_' + str(yon));
    assignMaterial('wood', obj);

    if yon is 2:  # sağ_yan
        obj.dimensions = (derinlik, kalinlik, yukseklik);
        obj.location = (-(derinlik / 2), -(kalinlik / 2), -(yukseklik / 2));
    elif yon is 3:  # ust
        obj.dimensions = (derinlik, modul_genislik, kalinlik);
        obj.location = ((-derinlik / 2), (-modul_genislik / 2), (-kalinlik / 2));
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
    collection.objects.link(obj);
    return obj


def collection_move(x, y, z, collection_adi):
    objects_sahne = bpy.data.collections[collection_adi].objects;

    for obj in objects_sahne:
        old_locationX, old_locationY, old_locationZ = obj.location;
        obj.location = (float(old_locationX - z), float(old_locationY - x), float(old_locationZ - y));


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
                                Obje_Olsutur(kalinlik=float(DataCollectionJson[key][dataName].get('kalınlık', 1.8)),
                                             derinlik=float(DataCollectionJson[key]['boy']),
                                             yukseklik=float(DataCollectionJson[key].get('en', 0)),
                                             modul_genislik=float(DataCollectionJson[key].get('boy', 0)),
                                             locationX=float(DataCollectionJson[key]['x_1']),
                                             locationY=float(DataCollectionJson[key]['y_1']),
                                             locationZ=float(DataCollectionJson[key]['z_1']),
                                             yon=int(DataCollectionJson[key].get('tip', 1)),
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

                                Obje_Olsutur(kalinlik=float(DataCollectionJson[key][dataName].get('kalınlık', 1.8)),
                                             derinlik=float(DataCollectionJson[key]['en']),
                                             yukseklik=float(DataCollectionJson[key].get('boy', 0)),
                                             modul_genislik=float(genislik),
                                             locationX=float(DataCollectionJson[key]['x_1']),
                                             locationY=float(DataCollectionJson[key]['y_1']),
                                             locationZ=float(DataCollectionJson[key]['z_1']),
                                             yon=int(DataCollectionJson[key].get('tip', 1)),
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
                                    kalinlik=float(DataCollectionJson[key][dataDict].get('malzeme', {"mn": 0,
                                                                                                     "kn": 0,
                                                                                                     "adı": "66_Kar Beyaz",
                                                                                                     "kalınlık": 1.8,
                                                                                                     "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8)),
                                    derinlik=float(DataCollectionJson[key][dataDict]['en']),
                                    yukseklik=float(DataCollectionJson[key][dataDict]['boy']),
                                    modul_genislik=float(DataCollectionJson[key][dataDict]['boy']),
                                    locationX=float(DataCollectionJson[key][dataDict]['x_1']),
                                    locationY=float(DataCollectionJson[key][dataDict]['y_1']),
                                    locationZ=float(DataCollectionJson[key][dataDict]['z_1']),
                                    yon=int(DataCollectionJson[key][dataDict].get('tip', 3)),
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
                                    Obje_Olsutur(kalinlik=float(element[keyData].get('malzeme', {"mn": 0,
                                                                                                 "kn": 0,
                                                                                                 "adı": "66_Kar Beyaz",
                                                                                                 "kalınlık": 1.8,
                                                                                                 "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8)),
                                        derinlik=float(element[keyData].get('en', 0)),
                                        yukseklik=float(element[keyData].get('boy')),
                                        modul_genislik=float(element[keyData].get('en', 0)),
                                        locationX=float(element[keyData].get('x_1', 50)),
                                        locationY=float(element[keyData].get('y_1', 0)),
                                        locationZ=float(element[keyData].get('z_1', 0)),
                                        yon=int(element[keyData].get('tip', 2)),
                                        isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                        collection=collection);
                                elif element[keyData].get('tip', 2) == 1:
                                    Obje_Olsutur(kalinlik=element[keyData].get('malzeme', {"mn": 0,
                                                                                           "kn": 0,
                                                                                           "adı": "66_Kar Beyaz",
                                                                                           "kalınlık": 1.8,
                                                                                           "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8),
                                        derinlik=float(element[keyData].get('en', 0)),
                                        yukseklik=float(element[keyData].get('en')),
                                        modul_genislik=float(element[keyData].get('boy', 0)),
                                        locationX=float(element[keyData].get('x_1', 50)),
                                        locationY=float(element[keyData].get('y_1', 0)),
                                        locationZ=float(element[keyData].get('z_1', 0)),
                                        yon=int(element[keyData].get('tip', 2)),
                                        isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                        collection=collection);
                                elif element[keyData].get('tip', 2) == 2:
                                    Obje_Olsutur(kalinlik=float(element[keyData].get('malzeme', {"mn": 0,
                                                                                                 "kn": 0,
                                                                                                 "adı": "66_Kar Beyaz",
                                                                                                 "kalınlık": 1.8,
                                                                                                 "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8)),
                                        derinlik=float(element[keyData].get('boy', 0)),
                                        yukseklik=float(element[keyData].get('en')),
                                        modul_genislik=float(element[keyData].get('boy', 0)),
                                        locationX=float(element[keyData].get('x_1', 50)),
                                        locationY=float(element[keyData].get('y_1', 0)),
                                        locationZ=float(element[keyData].get('z_1', 0)),
                                        yon=int(element[keyData].get('tip', 2)),
                                        isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                        collection=collection);
                                else:
                                    Obje_Olsutur(kalinlik=float(element[keyData].get('malzeme', {"mn": 0,
                                                                                                 "kn": 0,
                                                                                                 "adı": "66_Kar Beyaz",
                                                                                                 "kalınlık": 1.8,
                                                                                                 "image": "rgb(255,255,255)"}).get(
                                        'kalınlık', 1.8)),
                                        derinlik=float(element[keyData].get('en', 0)),
                                        yukseklik=float(element[keyData].get('boy')),
                                        modul_genislik=float(element[keyData].get('en', 0)),
                                        locationX=float(element[keyData].get('x_1', 50)),
                                        locationY=float(element[keyData].get('y_1', 0)),
                                        locationZ=float(element[keyData].get('z_1', 0)),
                                        yon=int(element[keyData].get('tip', 2)),
                                        isim=element[keyData].get('adı', 'Hatalı_Control_Et'),
                                        collection=collection);


def kameraOlustur():
    print('MODE ' + bpy.context.mode)
    bpy.ops.object.camera_add(enter_editmode=False, location=mathutils.Vector((-600.0, -180.0, -160.0)));
    bpy.context.view_layer.objects.active = bpy.data.objects['Camera']
    bpy.data.objects['Camera'].rotation_euler = mathutils.Euler(
        (math.radians(-90.0), math.radians(-180.0), math.radians(90.0)), 'XYZ')

    bpy.data.objects['Camera'].data.sensor_width = 50;


def renderAl(customerEmail, id):
    scene = bpy.data.scenes['Scene']
    scene.render.image_settings.file_format = 'PNG';
    global ImgFilePath

    ImgFilePath = 'D:\\blenderRenderImage\\' + customerEmail + '_' + id + '.png';

    scene.render.filepath = ImgFilePath

    bpy.ops.render.render(afterRender(), 'INVOKE_DEFAULT', write_still=True, use_viewport=True);
    return ImgFilePath


def afterRender():
    window = bpy.context.window_manager.windows[0]
    screen = window.screen

    o = {"window": window}

    return o


def assignMaterial(textureAdi='test', obj=bpy.context.active_object):
    obj.data.materials.append(bpy.data.materials[textureAdi]);


@persistent
def SendEmailToCustomer(dummy):
    print('Path : ' + ImgFilePath)

    emailGonder = Send(To='sarginlar@gmail.com',
                       ImgFolder=ImgFilePath,
                       name='MobilyaPlan_' + 'CustomerName')
    emailGonder.sendEmail();
    databaseItem.changeRenderStatus(CustomerId)


def createNewScene():
    new_scene = bpy.data.scenes.new(name='DENEME')
    bpy.context.window.scene = new_scene


@persistent
def trigger(dummy):
    print(CustomerId)
    elemet = DatabaseConnection.Collection()
    elemet.changeRenderStatus(CustomerId)


def deleteAllObject():
    collections = list(bpy.data.collections)
    objects = list(bpy.context.view_layer.objects)
    # clear collection
    for c in collections:
        bpy.data.collections.remove(c, do_unlink=True)

    for o in objects:
        bpy.data.objects.remove(o, do_unlink=True)


def sarginCizimCalistir():
    deleteAllObject()
    global databaseItem
    databaseItem = DatabaseConnection.Collection();
    isEmpty = databaseItem.getDataFromDatabase();
    mod_isim = [];
    count = 0;

    if not isEmpty:
        global CustomerId
        CustomerId = databaseItem.shortedData[0].get('databaseId')
        print(CustomerId)
        CustomerEmail = databaseItem.shortedData[0].get('musteriEmail', 'sarginlar@gmail.com')
        CustomerName = databaseItem.shortedData[0].get('musteriAdi', 'MobilyaPlan')

        print('CustomerName: ' + CustomerName)
        print('CustomerEmail: ' + CustomerEmail)

        for element in databaseItem.shortedData[0].get('databaseItems'):
            mod_isim.append(element.get('modül_adı'))
            ad = element['modül_adı'];

            for isim in mod_isim:
                if ad == isim:
                    ad = str(element.get('modül_adı')) + '_' + str(count);
                    count = count + 1;

            kutu_Olustur(element, ad);
            collection_move(element.get('x1'), element.get('y1'),
                            element.get('z1'),
                            ad);

        kameraOlustur();
        renderAl('sarginlar@gmail.com', '123')
        # Renderden sonra yapılcak iş - Function içerisinde dışardan parametre almıyor.
        # bpy.app.handlers.render_post.append(SendEmailToCustomer)
        bpy.app.handlers.render_post.append(trigger)



def every_50_seconds():
    sarginCizimCalistir()
    return 50.0


if __name__ == '__main__':
    sarginCizimCalistir()
    bpy.app.timers.register(every_50_seconds, first_interval=10)


class Send:
    def __init__(self, To, ImgFolder, name):
        self.To = 'sarginlar@gmail.com'
        self.ImgFolder = ImgFolder
        self.From = 'yusufsargin9@gmail.com'
        self.Name = name

    def sendEmail(self):
        print('ELEMENT ' + self.To, self.ImgFolder, self.Name)

        img_data = open(self.ImgFolder, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Teşekkür Ederiz.'
        msg['From'] = self.To
        msg['To'] = self.From

        text = MIMEText("Teşekkür Ederiz.")
        msg.attach(text)
        image = MIMEImage(img_data, name=self.Name)
        msg.attach(image)

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login('yusufsargin9@gmail.com', 'sargin_966')
        s.sendmail(self.From, self.To, msg.as_string())
        s.quit()
