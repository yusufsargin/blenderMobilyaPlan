import math
from random import randrange

import bpy
import mathutils


class Accessor:
    def __init__(self, wall1, wall2):
        self.kapakObjWall1 = [item for item in wall1 if item.location.y < -10 and 'kapak' in item.name]
        self.kapakObjWall2 = [item for item in wall2 if 'kapak' in item.name]
        self.kulpObj = []

    """
        @Return obj name str
    """

    def createNewCollection(self, CollectionName='Yusuf'):
        collection = bpy.data.collections.new(str(CollectionName));
        bpy.context.scene.collection.children.link(collection);
        return bpy.data.collections[CollectionName];

    def getKulpFromStorage(self, kulpName='kulp001'):
        filepath = "//" + kulpName + ".blend"

        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith(kulpName)]

        # link them to scene
        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                scene.collection.objects.link(obj)
                self.kulpObj.append(obj.name)

        return self.kulpObj

    def copyObject(self, obj, collection, texture='kulp'):
        scene = bpy.context.scene
        try:
            createdObj = obj.copy()
            createdObj.data = obj.data.copy()
            createdObj.name = 'kulp' + str(randrange(100))
            createdObj.data.materials.append(bpy.data.materials[texture]);
        except:
            print('COPY ERROR');

        collection.objects.link(createdObj)

        return createdObj

    def setPosition(self, obj, location=[0, 0, 0]):
        x, y, z = location

        obj.location = (x, y, z)

        return obj

    def setSizeObject(self, obj, size=[0, 0, 0]):
        dx, dy, dz = size

        obj.dimensions = (dx, dy, dz)

        return obj

    def verification(self, obj):
        return list(obj.objects) != []

    def transformObjRotate(self, obj, radiand=270, direction='Z'):
        """
        The Object to transform, should selected before use this function.
        import mathutils,import bpy and import math should add for stable work.
        """
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(state=True)

        switcher = {
            'X': mathutils.Euler((math.radians(radiand), 0, 0), 'XYZ')[0],
            'Y': mathutils.Euler((0, math.radians(radiand), 0), 'XYZ')[1],
            'Z': mathutils.Euler((0, 0, math.radians(radiand)), 'XYZ')[2],
        }

        """
        @return {'FINISHED'} 
        """
        return bpy.ops.transform.rotate(value=switcher.get(direction, 'Z'), orient_axis=direction,
                                        orient_type='GLOBAL',
                                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                        constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
                                        proportional_edit_falloff='SMOOTH', proportional_size=1,
                                        use_proportional_connected=False,
                                        use_proportional_projected=False);

    def executeOperation(self):
        kulp = bpy.data.objects[self.getKulpFromStorage()[0]]
        kulpCollection = self.createNewCollection('Kulplar')

        # Birinci duvar için kulplar
        for obj in self.kapakObjWall1:
            dx, dy, dz = obj.dimensions
            kx, ky, kz = obj.location

            copyObj = self.copyObject(kulp, kulpCollection)
            cx, cy, cz = copyObj.dimensions

            # Boy kapak
            if dz > dy:
                self.setPosition(copyObj, [kx - (cx / 2), ky - (dy / 2) + 3, kz])
                self.transformObjRotate(copyObj, 90, 'X')
                # Geniş kapak
            else:
                # Üst dolap
                if kz > -159:
                    copyObj = self.copyObject(kulp, kulpCollection)
                    self.setPosition(copyObj, [kx - (cx / 2), ky, kz - (dz / 2) + 3])
                # Alt Dolap
                else:
                    copyObj = self.copyObject(kulp, kulpCollection)
                    self.setPosition(copyObj, [kx - (cx / 2), ky, kz + (dz / 2) - 3])

        # 2.Duvar için kulplar
        for obj in self.kapakObjWall2:
            dx, dy, dz = obj.dimensions
            kx, ky, kz = obj.location

            copyObj = self.copyObject(kulp, kulpCollection)
            cx, cy, cz = copyObj.dimensions

            # Boy kapak
            if (dz - 20) > dy:
                self.setPosition(copyObj, [kx - (dy / 2) + 3, ky + (dx / 2), kz])
                self.transformObjRotate(copyObj, 90, 'X')
                # Geniş kapak
            else:
                # Üst dolap
                if kz > -159:
                    copyObj = self.copyObject(kulp, kulpCollection)
                    self.setPosition(copyObj, [kx - (cx / 2), ky + (dx / 2), kz - (dz / 2) + 3])
                    self.transformObjRotate(copyObj, 90, 'Z')
                # Alt Dolap
                else:
                    copyObj = self.copyObject(kulp, kulpCollection)
                    self.setPosition(copyObj, [kx - (cx / 2), ky + (dx / 2), kz + (dz / 2) - 3])
                    self.transformObjRotate(copyObj, 90, 'Z')


class Firin(Accessor):
    def __init__(self, wall1, wall2):
        super().__init__(wall1, wall2)
        self.firinAreaCollection = [item for item in bpy.data.collections if 'alt_fırın' in item.name]
        self.firinObj = []

    def getFirinFromStorage(self, firinName='firin', objName='Firin'):
        filepath = "//" + firinName + ".blend"

        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith(objName)]

        # link them to scene
        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                scene.collection.objects.link(obj)
                self.firinObj.append(obj.name)

        return self.firinObj

    def executeOperation(self):
        firin = bpy.data.objects[self.getFirinFromStorage()[0]]
        firin.location = (100, 100, 100)
        firinCollection = self.createNewCollection('Firinlar')

        for collection in self.firinAreaCollection:
            if self.verification(collection):
                copyObj = self.copyObject(firin, firinCollection)
                solYan = [item for item in list(collection.objects) if 'sol yan' in item.name]
                lx, ly, lz = solYan[0].location
                fdx, fdy, fdz = copyObj.dimensions

                copyObj.location = (lx, ly - (fdy / 2), lz)


class Buzdolabi(Accessor):
    def __init__(self, wall1, wall2):
        super().__init__(wall1, wall2)
        self.buzdolabiAreaCollection = [item for item in bpy.data.collections if 'buzdolabı' in item.name]
        self.buzdolabiObj = []

    def getBuzdolabiFromStorage(self, buzdolabiName='buzdolabi', objName='Buzdolabi_Obj'):
        filepath = "//" + buzdolabiName + ".blend"

        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith(objName)]

        # link them to scene
        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                scene.collection.objects.link(obj)
                self.buzdolabiObj.append(obj.name)

        return self.buzdolabiObj

    def executeOperation(self):
        buzdolabi = bpy.data.objects[self.getBuzdolabiFromStorage()[0]]
        buzdolabi.location = (100, 100, 100)
        buzdolabiCollection = self.createNewCollection('Buzdolaplari')

        for collection in self.buzdolabiAreaCollection:
            if self.verification(collection):
                copyObj = self.copyObject(buzdolabi, buzdolabiCollection)
                solYan = [item for item in list(collection.objects) if 'sol yan' in item.name]
                lx, ly, lz = solYan[0].location
                sdx, sdy, sdz = solYan[0].dimensions
                fdx, fdy, fdz = copyObj.dimensions

                copyObj.location = (lx, ly - (fdy / 2), lz)

                ldx, ldy, ldz = copyObj.location
                locationMinBuzZ = ldz - (fdz / 2)  # 260
                solYanMinZ = (lz - (sdz / 2))  # 280
                last = ldz - (abs(solYanMinZ) - abs(locationMinBuzZ))

                copyObj.location = (lx, ly - (fdy / 2) - (sdy / 2) - 2, last)


class BulasikMak(Accessor):
    def __init__(self, wall1, wall2):
        super().__init__(wall1, wall2)
        self.bulasikMakAreaCollection = [item for item in bpy.data.collections if 'Blşk' in item.name]
        self.bulasikMakObj = []

    def getBulasikMakFromStorage(self, buzdolabiName='bulasikmak', objName='BulasikMak_Obj'):
        filepath = "//" + buzdolabiName + ".blend"

        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith(objName)]

        # link them to scene
        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                scene.collection.objects.link(obj)
                self.bulasikMakObj.append(obj.name)

        return self.bulasikMakObj

    def executeOperation(self):
        bulasikMak = bpy.data.objects[self.getBulasikMakFromStorage()[0]]
        bulasikMak.location = (100, 100, 100)
        bulasikMakCollection = self.createNewCollection('BulasikMakleri')

        for collection in self.bulasikMakAreaCollection:
            if self.verification(collection):
                copyObj = self.copyObject(bulasikMak, bulasikMakCollection)
                solYan = [item for item in list(collection.objects) if 'sol yan' in item.name]
                lx, ly, lz = solYan[0].location
                dlx, dly, dlz = solYan[0].dimensions
                fdx, fdy, fdz = copyObj.dimensions

                copyObj.location = (lx, ly - (fdy / 2) - dly, lz)
