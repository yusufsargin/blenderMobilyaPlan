import bpy


class Walls():
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

    def centerPoint(self):
        return [(self.findMaxValue().get('maxX') - self.findMinValues().get('minX')) / 2,
                (self.findMaxValue().get('maxY') - self.findMinValues().get('minY')) / 2,
                (self.findMaxValue().get('maxZ') - self.findMinValues().get('minZ')) / 2]

    def createCubeObjInBlender(self, name='Cube', dimensions=[0, 0, 0], location=[0, 0, 0], texture='wall',
                               offSet=[0, 0, 0]):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False);
        obj = bpy.context.scene.objects["Cube"]  # Get the object
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.context.view_layer.objects.active = obj

        obj.name = name
        obj.dimensions = (dimensions[0] + offSet[0], dimensions[1] + offSet[1], dimensions[2] + offSet[2])
        obj.location = (location[0] - (offSet[0] / 2), location[1],
                        location[2] - (offSet[2] / 2))
        obj.data.materials.append(bpy.data.materials[texture])

        return obj

    def createBox(self, offset=[0, 0, 0]):
        maxPoints = self.findMaxValue()

        self.createCubeObjInBlender('Walls', [abs(maxPoints.get('maxX')), abs(maxPoints.get('maxY')),
                                              abs(maxPoints.get('maxZ'))],
                                    location=self.centerPoint(),
                                    offSet=offset)
