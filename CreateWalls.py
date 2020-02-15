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

    def drawCube(self):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False)
        obj = bpy.context.scene.objects['Cube']
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        return obj

    def createWallBox(self, yon='sol', kose=[0, 0, 'sag'], texture='wall', dimensions=[0, 0, 0], location=[0, 0, 0],
                      offset=[0, 0, 0], kaydir=[0, 0, 0], name='wall1'):
        obj = self.drawCube();
        obj.data.materials.append(bpy.data.materials[texture])
        obj.name = name
        x, y, z = dimensions
        lx, ly, lz = location
        koseX, koseY, koseTur = kose
        kaydirX, kaydirY, kaydirZ = kaydir
        offsetX, offsetY, offsetZ = offset

        if yon == 'sol':
            if (kose[0] != 0 or kose[1] != 0) and koseTur == 'sol':
                solObj = self.drawCube()
                solObj.name = 'solKose'
                solObj.data.materials.append(bpy.data.materials[texture])
                solObj.dimensions = (koseX, koseY, z + offset[2])
                solObj.location = (-(koseX / 2) + kaydirX, -(koseY / 2) + kaydirY, lz + (offsetZ / 2) + kaydirZ)
                # ---------------------------------------------------

            obj.dimensions = (x + offsetX, 1.8, z + offsetZ)
            obj.location = (
                lx - (offsetX / 2) + kaydirX, -1.8 + kaydirY,
                lz + (offsetZ / 2) + kaydirZ)
        elif yon == 'sag':
            if (kose[0] != 0 or kose[1] != 0) and koseTur == 'sag':
                sagObj = self.drawCube()
                sagObj.name = 'sagKose'
                sagObj.data.materials.append(bpy.data.materials[texture])
                sagObj.dimensions = (koseX, koseY, z + offsetZ)
                sagObj.location = (
                    -(koseX / 2) + kaydirX, (koseY / 2) + kaydirY + ((ly * 2) - offsetY),
                    lz + (offsetZ / 2) + kaydirZ)

            obj.dimensions = (x + offset[0], 1.8, z + offsetZ)
            obj.location = (lx - (offsetX / 2) + kaydirX, (ly * 2) - offsetY + kaydirY,
                            lz + (offsetZ / 2) + kaydirZ)
        elif yon == 'on':
            if kose[0] != 0 or kose[1] != 0 and koseTur == 'on':
                pass
            else:
                obj.dimensions = (1.8, y + offset[1], z + offset[2])
                obj.location = (
                    (lx * 2) - (offset[0]) + kaydir[0], ly - (offset[1] / 2) + kaydir[1],
                    lz + (offset[2] / 2) + kaydir[2])
        elif yon == 'arka':
            if (kose[0] != 0 or kose[1] != 0) and koseTur == 'arka':
                pass
            else:
                obj.dimensions = (1.8, y + offset[1], z + offset[2])
                obj.location = (
                    -1.8 + kaydir[0], ly - (offset[1] / 2) + kaydir[1], lz + (offset[2] / 2) + kaydir[2])
        else:
            print('Wall Error')
            return 'ERROR'

        return obj.location

    def createWalls(self, dimensions=[0, 0, 0], offset=[0, 0, 0], location=[0, 0, 0], texture='wall', kaydir=[0, 0, 0],
                    kose=[0, 0, 'sol']):
        # Sol Duvar-------------------------------
        solDuvar = self.createWallBox(yon='sol', kose=kose, texture=texture, dimensions=dimensions, location=location,
                                      offset=offset,
                                      kaydir=kaydir, name='wall1')
        # Arka Duvar---------------------------------
        arkaDuvar = self.createWallBox(yon='arka', kose=kose, texture=texture, dimensions=dimensions, location=location,
                                       offset=offset,
                                       kaydir=kaydir, name='wall2')
        # Sağ Duvar---------------------------------
        sagDuvar = self.createWallBox(yon='sag', kose=kose, texture=texture, dimensions=dimensions, location=location,
                                      offset=offset,
                                      kaydir=kaydir, name='wall3')
        # Ön Duvar---------------------------------
        onDuvar = self.createWallBox(yon='on', kose=kose, texture=texture, dimensions=dimensions, location=location,
                                     offset=offset,
                                     kaydir=kaydir, name='wall4')
        # ------------------------------------------------------------------------------------------------
        return {
            'solDuvar': [solDuvar.x, solDuvar.y, solDuvar.z],
            "arkaDuvar": [arkaDuvar.x, arkaDuvar.y, arkaDuvar.z],
            "sagDuvar": [sagDuvar.x, sagDuvar.y, sagDuvar.z],
            "onDuvar": [onDuvar.x, onDuvar.y, onDuvar.z]
        }

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

    def createBox(self, offset=[0, 0, 0], kaydir=[0, 0, 0], kose=[0, 0]):
        maxPoints = self.findMaxValue()

        """self.createCubeObjInBlender('Walls', [abs(maxPoints.get('maxX')), abs(maxPoints.get('maxY')),
                                              abs(maxPoints.get('maxZ'))],
                                    location=self.centerPoint(),
                                    offSet=offset)"""

        return self.createWalls([abs(maxPoints.get('maxX')), abs(maxPoints.get('maxY')),
                                 abs(maxPoints.get('maxZ'))], location=self.centerPoint(), offset=offset,
                                texture='wall',
                                kaydir=kaydir, kose=kose)
