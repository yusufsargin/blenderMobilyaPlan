import math

import bpy
import mathutils


class WallOtherSide:
    def __init__(self, items):
        self.items = items

    def transformObjRotate(self, radiand=270, direction='Z'):
        """
        The Object to transform, should selected before use this function.
        import mathutils,import bpy and import math should add for stable work.
        """

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

    def transformObjMove(self, vector=(0, 0, 0)):
        return bpy.ops.transform.translate(value=vector, orient_type='GLOBAL',
                                           orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                           constraint_axis=(False, True, False), mirror=True,
                                           use_proportional_edit=False, proportional_edit_falloff='SMOOTH',
                                           proportional_size=1, use_proportional_connected=False,
                                           use_proportional_projected=False)

    def findMinValues(self):
        minZVal = 0
        minXVal = 0
        minYVal = 0

        for obj in self.items:
            x, y, z = obj.location
            dX, dY, dZ = obj.dimensions

            if minZVal < (z + (dZ / 2)):
                minZVal = (z + (-dZ / 2))
            if minXVal < (x + (dX / 2)):
                minXVal = (x + (dX / 2))
            if minYVal < (y + (dY / 2)):
                minYVal = (y + (dY / 2))

        return {
            "minX": minXVal,
            "minY": minYVal,
            "minZ": minZVal
        }

    def findMaxValue(self):
        maxZVal = 0;
        maxXVal = 0;
        maxYVal = 0;

        for obj in self.items:
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

    def centerPoint(self):
        return [(self.findMaxValue().get('maxX') - self.findMinValues().get('minX')) / 2,
                (self.findMaxValue().get('maxY') - self.findMinValues().get('minY')) / 2,
                (self.findMaxValue().get('maxZ') - self.findMinValues().get('minZ')) / 2]

    def selectObj(self):
        bpy.ops.object.select_all(action='DESELECT')

        for o in self.items:
            o.select_set(state=True)

        return bpy.context.selectable_objects

    def execute(self, corner=[0, 0, 'sag'], wallLocation={'sagDuvar': [0, 0, 0]}):
        if len(self.items) != 0:
            cX, cY, cSide = corner

            if cSide == 'sag':
                wallX, wallY, wallZ = wallLocation.get('sagDuvar', [0, 0, 0])
                self.selectObj()
                if cX != 0 or cY != 0:
                    self.transformObjRotate(270, 'Z')

                    minValue = self.findMinValues()
                    minX = minValue.get('minX', 0)
                    minY = minValue.get('minY', 0)
                    minZ = minValue.get('minZ', 0)

                    # sadece x üzerinde kaydırma yapılıyor.
                    x, y, z = [-(minX + cX), (minY + (wallY / 2)), 0]

                    self.transformObjMove((x, y, z))

                    koseObj = [item for item in bpy.data.objects if 'Kose' in item.name][0]
                    koseMax = koseObj.location.x - (koseObj.dimensions.x / 2)
                    firstObj = [item for item in bpy.data.objects if 'boşluk' in item.name and item.dimensions != 0]
                    if len(firstObj) != 0:
                        firstMin = firstObj[0].location.x + (firstObj[0].dimensions.y / 2)

                        diff = koseMax - firstMin

                        self.selectObj()
                        self.transformObjMove(vector=(diff, 0, 0))

                        self.selectObj()
                        self.transformObjMove(vector=(firstObj[0].dimensions.y, wallY - firstObj[0].location.y, 0))

                    return 'SUCCESS'
