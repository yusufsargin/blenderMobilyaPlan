import bpy


class Walls():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def findMinPoints(self):
        minPoints = {
            "minX": 0,
            "minY": 0,
            "minZ": 0
        }

        for obj in bpy.data.objects:
            x, y, z = obj.dimensions
            lx, ly, lz = obj.location
            # for x
            if minPoints.get('minX', 0) > abs(lx):
                minPoints['minX'] = lx + (x / 2)
            # for y
            if minPoints.get('minY', 0) > abs(ly):
                minPoints['minY'] = ly + (y / 2)
            if minPoints.get('minZ') < abs(lz):
                minPoints['minZ'] = lz - (z / 2)

        return minPoints

    def findMaxPoints(self):
        maxPoints = {
            "maxX": 0,
            "maxY": 0,
            "maxZ": 0
        }

        for obj in bpy.data.objects:
            x, y, z = obj.dimensions
            lx, ly, lz = obj.location
            # for x
            if maxPoints.get('maxX', 0) < abs(lx):
                maxPoints['maxX'] = lx - (x / 2)
            # for y
            if maxPoints.get('maxY', 0) < abs(ly):
                maxPoints['maxY'] = ly - (y / 2)
            if maxPoints.get('maxZ') > abs(lz):
                maxPoints['maxZ'] = lz + (z / 2)

        return maxPoints

    def createCubeObjInBlender(self, name='Cube', dimensions=[0, 0, 0], location=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False);
        obj = bpy.context.scene.objects["Cube"]  # Get the object
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.context.view_layer.objects.active = obj

        obj.name = name
        obj.dimensions = (dimensions[0], dimensions[1], dimensions[2])
        obj.location = (location[0], location[1], location[2])

        return obj

    def createBox(self):
        minPoints = self.findMinPoints()
        maxPoints = self.findMaxPoints()
