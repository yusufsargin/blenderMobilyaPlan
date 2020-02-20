import math
from random import randrange

import bpy
import mathutils


class Accessor:
    def __init__(self, wall1, wall2):
        self.kapakObjWall1 = wall1
        self.kapakObjWall2 = wall2
        self.kulpObj = []

    def getKulpFromStorage(self, kulpName='kulp001'):
        filepath = "//" + kulpName + ".blend"

        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith(kulpName)]

        # link them to scene
        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                scene.collection.objects.link(obj)
                self.kulpObj.append(obj)

        return self.kulpObj

    def copyObject(self, obj):
        scene = bpy.context.scene

        createdObj = obj.copy()
        createdObj.data = obj.data.copy()
        createdObj.name = 'kulp' + str(randrange(100))
        scene.objects.link(createdObj)
        return createdObj

    def setPosition(self, obj, location=[0, 0, 0]):
        x, y, z = location

        obj.location = (x, y, z)

        return obj

    def setSizeObject(self, obj, size=[0, 0, 0]):
        dx, dy, dz = size

        obj.dimensions = (dx, dy, dz)

        return obj

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
        return bpy.ops.transform.rotate(value=switcher.get(direction, 'Z'), orient_axis='Z',
                                        orient_type='GLOBAL',
                                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                        constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
                                        proportional_edit_falloff='SMOOTH', proportional_size=1,
                                        use_proportional_connected=False,
                                        use_proportional_projected=False);

    def executeOperation(self):
        kulp = self.getKulpFromStorage()[0]

        for obj in self.kapakObjWall1:
            dx, dy, dz = obj.dimensions
            kx, ky, kz = obj.location

            # Boy kapak
            if dz > dy:
                copyObj = self.copyObject(kulp)
                self.setPosition(copyObj, [kx, ky - (ky / 2), kz])
                self.transformObjRotate(copyObj, 90, 'X')
            # Geniş kapak
            elif dx > dz:
                copyObj = self.copyObject(kulp)
                self.setPosition(copyObj, [kx, ky, kz + (kz / 2)])
