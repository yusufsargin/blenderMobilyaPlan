import math
from random import randrange

import bpy
import mathutils
from bpy.app.handlers import persistent

import DatabaseConnection
import DrawEngine
from AccessorSettings import Accessor
from AccessorSettings import BulasikMak
from AccessorSettings import Buzdolabi
from AccessorSettings import Firin
from CreateWallAsideObject import WallOtherSide
from CreateWalls import Walls

standard_kalinlik = 0.018;
standard_derinlik = 0.60;
standard_yukseklik = 0.75;
standard_genislik = 0.65;
sahnedeki_objeler = [];

bl_info = {
    "name": "Sargin Render",
    "author": "Yusuf Sargin",
    "version": (0, 5, 6, 6),
    "blender": (2, 8, 0)
}

config = {
    "renderAcik": False
}


class SarginDraw():
    def __init__(self):
        self.isRender = True
        self.wall2 = []
        self.wall1 = []
        self.wall1Kapak = []
        self.wall2Kapak = []

    def setPostionObj(self, obj, locationX, locationY, locationZ):
        dx, dy, dz = obj.dimensions
        obj.location = ((-dx / 2), (-dy / 2), (-dz / 2))

        x, y, z = obj.location

        obj.location = ((x - locationZ), (y - locationX), (z - locationY))

    def make_offset(self, obj, yon=1, ust=0, yan=0):
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

    def drawTezgah(self, isim='mobilyaPlanTezgah', texture='mermer1', yon='3', derinlik=0, modul_genislik=0,
                   kalinlik=1.8,
                   locationX=0, locationY=0, locationZ=0, collection=[], wallType='0'):
        bpy.ops.mesh.primitive_cube_add(size=2)
        obj = bpy.context.scene.objects['Cube']
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = obj
        obj.name = str(isim + '_' + str(yon))
        self.assignMaterial(texture, obj)

        obj.dimensions = (derinlik, modul_genislik, kalinlik)
        obj.location = ((-derinlik / 2), (-modul_genislik / 2), (-kalinlik / 2))

        x, y, z = obj.location
        obj.location = ((x - locationZ), (y - locationX), (z - locationY))
        collection.objects.link(obj)
        if int(wallType) == 1:
            self.wall2.append(obj)

    def Obje_Olsutur(self, kalinlik=standard_kalinlik, derinlik=standard_derinlik, yukseklik=standard_yukseklik,
                     modul_genislik=0, locationX=0, locationY=0, locationZ=0, isim='Sargın',
                     collection=[],
                     yon=1, texture='wood', wallType='0'):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False);
        obj = bpy.context.scene.objects["Cube"]  # Get the object
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.context.view_layer.objects.active = obj
        obj.name = str(isim + '_' + str(yon) + '_' + str(randrange(100)));
        self.assignMaterial(texture, obj);

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
            print('\n');

        if (locationX is not 0) or (locationY is not 0) or (locationZ is not 0):
            x, y, z = obj.location;
            if yon is 1:
                obj.location = ((x - locationZ), (y - locationX), (z - locationY));
            elif yon is 3:
                obj.location = ((x - locationZ), (y - locationX), (z - locationY));
            else:
                obj.location = ((x - locationZ), (y - locationX), (z - locationY));

        sahnedeki_objeler.append(obj)
        collection.objects.link(obj)

        if int(wallType) == 1 and ('kapak' in obj.name):
            self.wall2.append(obj)
        elif int(wallType) == 0 and ('kapak' in obj.name):
            self.wall1.append(obj)
        return obj

    def collection_move(self, x, y, z, collection_adi):
        objects_sahne = bpy.data.collections[collection_adi].objects;

        for obj in objects_sahne:
            old_locationX, old_locationY, old_locationZ = obj.location;
            obj.location = (float(old_locationX - z), float(old_locationY - x), float(old_locationZ - y));

    def createNewCollection(self, CollectionName='Yusuf'):
        collection = bpy.data.collections.new(str(CollectionName));
        bpy.context.scene.collection.children.link(collection);
        return bpy.data.collections[CollectionName];

    def tezgahOlustur(self, DataCollectionJson, CollectionName='Yusuf'):
        collection = self.createNewCollection(CollectionName);

        for key in DataCollectionJson:
            wallType = DataCollectionJson.get('duvar_no', '0');
            if key == 'tezgah' and DataCollectionJson[key].get('dahil', False) == True:
                for data in DataCollectionJson[key]:
                    if type(DataCollectionJson[key].get(data)) == dict and DataCollectionJson[key].get(data).get(
                            'dahil',
                            False) == True:
                        if DataCollectionJson[key].get(data).get('tip') == 3:
                            genislik = DataCollectionJson[key].get(data).get('boy');
                        else:
                            genislik = DataCollectionJson[key].get(data).get('en');

                        self.Obje_Olsutur(kalinlik=float(DataCollectionJson[key].get(data).get('kalınlık', 3)),
                                          derinlik=float(DataCollectionJson[key].get(data).get('en')),
                                          yukseklik=float(DataCollectionJson[key].get(data).get('boy', 0)),
                                          modul_genislik=float(genislik),
                                          locationX=float(DataCollectionJson[key].get(data).get('x_1')),
                                          locationY=float(DataCollectionJson[key].get(data).get('y_1')),
                                          locationZ=float(DataCollectionJson[key].get(data).get('z_1')),
                                          yon=int(DataCollectionJson[key].get(data).get('tip', 3)),
                                          isim=DataCollectionJson[key].get(data).get('adı'), collection=collection,
                                          texture='mermerBeyaz', wallType=wallType);

    def kutu_Olustur(self, DataCollectionJson, CollectionName='Yusuf'):
        collection = self.createNewCollection(CollectionName);
        for key in DataCollectionJson.keys():
            wallType = DataCollectionJson.get('duvar_no', '0')

            if type(DataCollectionJson[key]) is dict:
                topOfItem = list(DataCollectionJson[key].keys());
                if DataCollectionJson[key].get('dahil', False):
                    # normal sol-sag-raf cizimler
                    for dataName in topOfItem:
                        if type(DataCollectionJson[key][dataName]) is dict:
                            if dataName == 'malzeme':
                                # baza ve arka kuşak için çizim
                                if ('baza' in DataCollectionJson[key].get('adı', 'HATA') or 'arka kuşak' in
                                        DataCollectionJson[key].get('adı', 'HATA')):
                                    self.Obje_Olsutur(
                                        kalinlik=float(DataCollectionJson[key][dataName].get('kalınlık', 1.8)),
                                        derinlik=float(DataCollectionJson[key]['boy']),
                                        yukseklik=float(DataCollectionJson[key].get('en', 0)),
                                        modul_genislik=float(DataCollectionJson[key].get('boy', 0)),
                                        locationX=float(DataCollectionJson[key]['x_1']),
                                        locationY=float(DataCollectionJson[key]['y_1']),
                                        locationZ=float(DataCollectionJson[key]['z_1']),
                                        yon=int(DataCollectionJson[key].get('tip', 1)),
                                        isim=DataCollectionJson[key]['adı'], collection=collection, wallType=wallType);
                                else:
                                    if DataCollectionJson[key].get('tip') == 3:
                                        genislik = DataCollectionJson[key].get('boy');
                                    else:
                                        genislik = DataCollectionJson[key].get('en');

                                    self.Obje_Olsutur(
                                        kalinlik=float(DataCollectionJson[key][dataName].get('kalınlık', 1.8)),
                                        derinlik=float(DataCollectionJson[key]['en']),
                                        yukseklik=float(DataCollectionJson[key].get('boy', 0)),
                                        modul_genislik=float(genislik),
                                        locationX=float(DataCollectionJson[key]['x_1']),
                                        locationY=float(DataCollectionJson[key]['y_1']),
                                        locationZ=float(DataCollectionJson[key]['z_1']),
                                        yon=int(DataCollectionJson[key].get('tip', 1)),
                                        isim=DataCollectionJson[key]['adı'], collection=collection, wallType=wallType);

                # Üst Ve Alt çizimi için
                else:
                    # üst çizim
                    for dataDict in topOfItem:
                        if type(DataCollectionJson[key][dataDict]) is dict and type(
                                DataCollectionJson[key][dataDict]) is not int:
                            if DataCollectionJson[key][dataDict].get('dahil', False) is True:
                                if (dataDict != 'kulp'):
                                    self.Obje_Olsutur(
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
                                        collection=collection, wallType=wallType);

            elif (type(DataCollectionJson[key]) == list):
                for element in DataCollectionJson[key]:
                    if type(element) == dict:
                        for keyData in element.keys():
                            if type(element[keyData]) == dict:
                                if element[keyData].get('dahil', False) == True:
                                    # Kapak  çizim
                                    if 'kapak' in keyData:
                                        self.Obje_Olsutur(kalinlik=float(element[keyData].get('malzeme', {"mn": 0,
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
                                            collection=collection, wallType=wallType);
                                    elif element[keyData].get('tip', 2) == 1:
                                        self.Obje_Olsutur(kalinlik=element[keyData].get('malzeme', {"mn": 0,
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
                                            collection=collection, wallType=wallType);
                                    elif element[keyData].get('tip', 2) == 2:
                                        self.Obje_Olsutur(kalinlik=float(element[keyData].get('malzeme', {"mn": 0,
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
                                            collection=collection, wallType=wallType);
                                    else:
                                        self.Obje_Olsutur(kalinlik=float(element[keyData].get('malzeme', {"mn": 0,
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
                                            collection=collection, wallType=wallType);

    def kameraOlustur(self):
        print('MODE ' + bpy.context.mode)
        bpy.ops.object.camera_add(enter_editmode=False, location=mathutils.Vector((-600.0, -180.0, -160.0)));
        bpy.context.view_layer.objects.active = bpy.data.objects['Camera']
        bpy.data.objects['Camera'].rotation_euler = mathutils.Euler(
            (math.radians(-90.0), math.radians(-180.0), math.radians(90.0)), 'XYZ')

        bpy.data.objects['Camera'].data.sensor_width = 50;

    def renderAl(self, customerEmail, id):
        scene = bpy.data.scenes['Scene']
        scene.render.image_settings.file_format = 'PNG';

        global ImgFilePath
        global CustomerEmail
        global CustomerID
        global imgName

        CustomerEmail, CustomerID = self.CustomerEmail, self.CustomerId

        ImgFilePath = 'D:\\blenderRenderImage\\' + CustomerEmail + '_' + CustomerID + '.png';

        scene.render.filepath = ImgFilePath
        imgName = CustomerEmail + '_' + CustomerID + '.png'

        bpy.ops.render.render(self.afterRender(), 'INVOKE_DEFAULT', write_still=True, use_viewport=True);
        return ImgFilePath

    def afterRender(self):
        window = bpy.context.window_manager.windows[0]
        screen = window.screen

        o = {"window": window}

        return o

    def createWall(self, offSetX, offSetY):
        bpy.ops.mesh.primitive_plane_add(size=10)
        obj = bpy.data.objects['Plane']
        obj.name = 'Wall'

        dx = -self.findMaxValue().get('maxX') + offSetX
        dy = -self.findMaxValue().get('maxY') + offSetY
        dz = -self.findMaxValue().get('maxZ')

        obj.dimensions = (dx, dy, dz)
        obj.location = (
            self.findMinValues().get('minY'), -(dy / 2) + (offSetY / 2), self.findMaxValue().get('maxZ') + offSetY)
        obj.rotation_euler = mathutils.Euler(
            (math.radians(-90.0), math.radians(-180.0), math.radians(90.0)), 'XYZ')
        obj.data.materials.append(bpy.data.materials['wall'])

    def assignMaterial(self, textureAdi='test', obj=bpy.context.active_object):
        obj.data.materials.append(bpy.data.materials[textureAdi])

    @persistent
    def SendEmailToCustomer(self, dummy):
        print('Path : ' + ImgFilePath)

        databaseItem.changeRenderStatus(CustomerID)
        databaseItem.saveImage(imgName=imgName, imgFilePath=ImgFilePath, id=CustomerID)
        self.isRender = True

    def createNewScene(self):
        new_scene = bpy.data.scenes.new(name='DENEME')
        bpy.context.window.scene = new_scene

    def deleteAllObject(self):
        collections = list(bpy.data.collections)
        objects = list(bpy.context.view_layer.objects)
        # clear collection
        for c in collections:
            bpy.data.collections.remove(c, do_unlink=True)

        for o in objects:
            bpy.data.objects.remove(o, do_unlink=True)

    def findMinValues(self):
        minZVal = 0;
        minXVal = 0;
        minYVal = 0;

        for obj in bpy.data.objects:
            x, y, z = obj.location
            dX, dY, dZ = obj.dimensions

            if minZVal < (z - (-dZ / 2)):
                minZVal = -(z - (-dZ / 2))
            if minXVal < (x - (-dX / 2)):
                minXVal = -(x - (-dX / 2))
            if minYVal < (y - (dY / 2)):
                minYVal = -(y - (dY / 2))

        print('MIN ' + str(minXVal) + ',' + str(minYVal) + ',' + str(minZVal))

        return {
            "minX": minXVal,
            "minY": minYVal,
            "minZ": minZVal
        }

    def findMaxValue(self):
        maxZVal = 0;
        maxXVal = 0;
        maxYVal = 0;

        for obj in bpy.data.objects:
            x, y, z = obj.location
            dX, dY, dZ = obj.dimensions

            if maxZVal > (z - (dZ / 2)):
                maxZVal = z - (dZ / 2)
            if maxXVal > x - (dX / 2):
                maxXVal = x - (dX / 2)
            if maxYVal < -(y - (-dY / 2)):
                maxYVal = -(y + (-dY / 2))

        print('MAX ' + str(maxXVal) + ',' + str(maxYVal) + ',' + str(maxZVal))

        return {
            "maxX": maxXVal,
            "maxY": -maxYVal,
            "maxZ": maxZVal
        }

    def createFloor(self, offSet):
        bpy.ops.mesh.primitive_plane_add(size=10)
        obj = bpy.data.objects['Plane']
        obj.name = 'Floor'

        dx = -self.findMaxValue().get('maxX') + offSet
        dy = -self.findMaxValue().get('maxY') + offSet
        dz = -self.findMaxValue().get('maxZ') + offSet

        obj.dimensions = (dx, dy, dz)
        obj.location = (-(dx / 2), -(dy / 2) + (offSet / 2), self.findMaxValue().get('maxZ'))
        obj.data.materials.append(bpy.data.materials['floor'])

    def getFirinObj(self, element):
        filepath = "//firin.blend"

        # append all objects starting with 'house'
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("Firin")]

        # link them to scene
        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                self.setPostionObj(obj, element.get('x_1'), element.get('y_1'), element.get('z_1'))
                scene.collection.objects.link(obj)

    def sarginCizimCalistir(self):

        if self.isRender:
            print(self.isRender)
            print('\n')
            self.isRender = False
            self.deleteAllObject()
            global databaseItem
            databaseItem = DatabaseConnection.Collection();
            isEmpty = databaseItem.getDataFromDatabase();
            mod_isim = [];
            count = 0;

            if not isEmpty:
                self.CustomerId = databaseItem.shortedData[0].get('databaseId')
                print(self.CustomerId)
                self.CustomerEmail = databaseItem.shortedData[0].get('musteriEmail', 'sarginlar@gmail.com')
                self.CustomerName = databaseItem.shortedData[0].get('musteriAdi', 'MobilyaPlan')

                print('CustomerName: ' + self.CustomerName)
                print('CustomerEmail: ' + self.CustomerEmail)

                drawEngine = DrawEngine.CreateObject(databaseItem.shortedData[0].get('databaseItems'))
                drawEngine.dataOrganize()
                """for element in databaseItem.shortedData[0].get('databaseItems'):
                    mod_isim.append(element.get('modül_adı'))
                    ad = element.get('modül_adı', 'HATA');

                    for isim in mod_isim:
                        if ad == isim:
                            ad = str(element.get('modül_adı')) + '_' + str(randrange(100))
                            count = count + 1;

                    #self.kutu_Olustur(element, ad);
                    drawEngine
                    self.tezgahOlustur(element, ad)
                    self.collection_move(element.get('x1'), element.get('y1'),
                                         element.get('z1'),
                                         ad);"""

                wall = Walls()

                self.wall1 = drawEngine.wall1
                self.wall2 = drawEngine.wall2

                bosluk = [item for item in self.wall2 if 'boşluk_1' in item.name]

                if bosluk != []:
                    koseX, koseY, koseTur = [bosluk[0].dimensions.y, 60, 'sag']
                    offsetX, offsetY, offsetZ = [300, 50, 0]
                    kaydirX, kaydirY, kaydirZ = [0, 50, 0]
                else:
                    koseX, koseY, koseTur = [100, 60, 'sag']
                    offsetX, offsetY, offsetZ = [300, 50, 0]
                    kaydirX, kaydirY, kaydirZ = [0, 50, 0]

                if koseTur == 'sol':
                    wallLocation = wall.createBox(offset=[offsetX, offsetY + koseY, offsetZ],
                                                  kaydir=[kaydirX, kaydirY + koseY, kaydirZ],
                                                  kose=[koseX, koseY, koseTur])
                elif koseTur == 'sag':
                    wallLocation = wall.createBox(offset=[offsetX, offsetY + koseY, offsetZ],
                                                  kaydir=[kaydirX, kaydirY, kaydirZ],
                                                  kose=[koseX, koseY, koseTur])
                else:
                    wallLocation = wall.createBox(offset=[offsetX, offsetY, offsetZ],
                                                  kaydir=[kaydirX, kaydirY, kaydirZ],
                                                  kose=[koseX, koseY, koseTur])

                # wall.createBox(offset=[0, 0 + kose[1], 0], kaydir=[0, 0 + kose[1], 0], kose=kose)

                asizeWall = WallOtherSide(self.wall2)

                if len(self.wall2) != 0:
                    print(self.wall2)
                    print(wallLocation)
                    asizeWall.execute([koseX, koseY, koseTur], wallLocation)

                self.createFloor(500)

                aksesuar = Accessor(self.wall1, self.wall2)
                aksesuar.executeOperation()

                firin = Firin(self.wall1, self.wall2)
                buzdolabi = Buzdolabi(self.wall1, self.wall2)
                bulasikMak = BulasikMak(self.wall1, self.wall2)
                bulasikMak.executeOperation()
                buzdolabi.executeOperation()
                firin.executeOperation()

                self.kameraOlustur()
                if config['renderAcik']:
                    self.renderAl(self.CustomerEmail, self.CustomerId)
                    # Renderden sonra yapılcak iş - Function içerisinde dışardan parametre almıyor.
                    bpy.app.handlers.render_post.append(self.SendEmailToCustomer)

    def every_10_seconds(self):
        self.sarginCizimCalistir()
        return 10.0

    def start(self):
        """self.deleteAllObject()
        self.getFirinObj()"""
        bpy.app.timers.register(self.every_10_seconds, first_interval=10)


def every_30_seconds():
    cizim = SarginDraw()
    cizim.sarginCizimCalistir()
    del cizim
    return 30.0


if __name__ == '__main__':
    cizim = SarginDraw()
    cizim.sarginCizimCalistir()

    if config['renderAcik']:
        bpy.app.timers.register(every_30_seconds, first_interval=10)
