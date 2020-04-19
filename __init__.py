import math

import bpy
import mathutils
from bpy.app.handlers import persistent

from Accesories.AccessorSettings import Accessor
from Accesories.AccessorSettings import BulasikMak
from Accesories.AccessorSettings import Buzdolabi
from Accesories.AccessorSettings import Firin
from DatabaseModel import DatabaseConnection
from DrawEngineCollector import DrawEngine
from WallOperation.CreateWallAsideObject import WallOtherSide
from WallOperation.CreateWalls import Walls

standard_kalinlik: float = 0.018
standard_derinlik: float = 0.60
standard_yukseklik: float = 0.75
standard_genislik: float = 0.65
sahnedeki_objeler: list = []

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
        x, y, z = obj.dimensions
        if ust is not 0:
            if yon is 1:
                obj.dimensions = (x, y, abs(z - (ust * 2)))
            elif yon is 2:
                obj.dimensions = (x, abs(y - (ust * 2)), z)
            elif yon is 3:
                obj.dimensions = (x, y, abs(z - (ust * 2)))
        elif yan is not 0:
            if yon is 1:
                obj.dimensions = (abs(x - (yan * 2)), y, z)
            elif yon is 2:
                obj.dimensions = (abs(x - (yan * 2)), y, z)
            elif yon is 3:
                obj.dimensions = (x, abs(y - (yan * 2)), z)

    def kameraOlustur(self):
        bpy.ops.object.camera_add(enter_editmode=False, location=mathutils.Vector((-600.0, -180.0, -160.0)))
        bpy.context.view_layer.objects.active = bpy.data.objects['Camera']
        bpy.data.objects['Camera'].rotation_euler = mathutils.Euler(
            (math.radians(-90.0), math.radians(-180.0), math.radians(90.0)), 'XYZ')

        bpy.data.objects['Camera'].data.sensor_width = 50

    def renderAl(self, customerEmail, id):
        scene = bpy.data.scenes['Scene']
        scene.render.image_settings.file_format = 'PNG'

        global ImgFilePath
        global CustomerEmail
        global CustomerID
        global imgName

        CustomerEmail, CustomerID = self.CustomerEmail, self.CustomerId

        ImgFilePath = 'D:\\blenderRenderImage\\' + CustomerEmail + '_' + CustomerID + '.png'

        scene.render.filepath = ImgFilePath
        imgName = CustomerEmail + '_' + CustomerID + '.png'

        bpy.ops.render.render(self.afterRender(), 'INVOKE_DEFAULT', write_still=True, use_viewport=True)
        return ImgFilePath

    @staticmethod
    def afterRender():
        window = bpy.context.window_manager.windows[0]
        screen = window.screen

        o = {"window": window}

        return o

    @persistent
    def SendEmailToCustomer(self, dummy):
        print('Path : ' + ImgFilePath)

        databaseItem.changeRenderStatus(CustomerID)
        databaseItem.saveImage(imgName=imgName, imgFilePath=ImgFilePath, id=CustomerID)
        self.isRender = True

    def deleteAllObject(self):
        collections = list(bpy.data.collections)
        objects = list(bpy.context.view_layer.objects)
        # clear collection
        for c in collections:
            bpy.data.collections.remove(c, do_unlink=True)

        for o in objects:
            bpy.data.objects.remove(o, do_unlink=True)

    def findMinValues(self) -> dict:
        minZVal = 0
        minXVal = 0
        minYVal = 0

        for obj in bpy.data.objects:
            x, y, z = obj.location
            dX, dY, dZ = obj.dimensions

            if minZVal < (z - (-dZ / 2)):
                minZVal = -(z - (-dZ / 2))
            if minXVal < (x - (-dX / 2)):
                minXVal = -(x - (-dX / 2))
            if minYVal < (y - (dY / 2)):
                minYVal = -(y - (dY / 2))

        return {
            "minX": minXVal,
            "minY": minYVal,
            "minZ": minZVal
        }

    def findMaxValue(self) -> dict:
        maxZVal: float = 0
        maxXVal: float = 0
        maxYVal: float = 0

        for obj in bpy.data.objects:
            x, y, z = obj.location
            dX, dY, dZ = obj.dimensions

            if maxZVal > (z - (dZ / 2)):
                maxZVal = z - (dZ / 2)
            if maxXVal > x - (dX / 2):
                maxXVal = x - (dX / 2)
            if maxYVal < -(y - (-dY / 2)):
                maxYVal = -(y + (-dY / 2))

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

    def sarginCizimCalistir(self):
        if self.isRender:
            self.isRender = False
            self.deleteAllObject()
            global databaseItem
            databaseItem = DatabaseConnection.Collection()
            isEmpty = databaseItem.getDataFromDatabase()

            if not isEmpty:
                self.CustomerId = databaseItem.shortedData[0].get('databaseId')
                print(self.CustomerId)
                self.CustomerEmail = databaseItem.shortedData[0].get('musteriEmail', 'sarginlar@gmail.com')
                self.CustomerName = databaseItem.shortedData[0].get('musteriAdi', 'MobilyaPlan')

                print('CustomerName: ' + self.CustomerName)
                print('CustomerEmail: ' + self.CustomerEmail)

                drawEngine = DrawEngine.CreateObject(databaseItem.shortedData[0].get('databaseItems', {}))
                drawEngine.dataOrganize()

                wall = Walls()

                self.wall1 = drawEngine.wall1
                self.wall2 = drawEngine.wall2

                bosluk = [item for item in self.wall2 if 'boşluk' in item.name]

                if len(bosluk) != 0:
                    offsetX, offsetY, offsetZ = [300, 50, 0]
                    kaydirX, kaydirY, kaydirZ = [0, 50, 0]
                    koseX, koseY, koseTur = [bosluk[0].dimensions.y, 60, 'sag']
                else:
                    offsetX, offsetY, offsetZ = [300, 50, 0]
                    kaydirX, kaydirY, kaydirZ = [0, 50, 0]
                    koseX, koseY, koseTur = [100, 60, 'sag']

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
