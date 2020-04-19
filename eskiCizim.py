def tezgahOlustur(self, DataCollectionJson, CollectionName='Yusuf'):
    collection = self.createNewCollection(CollectionName)

    for key in DataCollectionJson:
        wallType = DataCollectionJson.get('duvar_no', '0')
        if key == 'tezgah' and DataCollectionJson[key].get('dahil', False) == True:
            for data in DataCollectionJson[key]:
                if type(DataCollectionJson[key].get(data)) == dict and DataCollectionJson[key].get(data).get(
                        'dahil',
                        False) == True:
                    if DataCollectionJson[key].get(data).get('tip') == 3:
                        genislik = DataCollectionJson[key].get(data).get('boy')
                    else:
                        genislik = DataCollectionJson[key].get(data).get('en')

                    self.Obje_Olsutur(kalinlik=float(DataCollectionJson[key].get(data).get('kalınlık', 3)),
                                      derinlik=float(DataCollectionJson[key].get(data).get('en')),
                                      yukseklik=float(DataCollectionJson[key].get(data).get('boy', 0)),
                                      modul_genislik=float(genislik),
                                      locationX=float(DataCollectionJson[key].get(data).get('x_1')),
                                      locationY=float(DataCollectionJson[key].get(data).get('y_1')),
                                      locationZ=float(DataCollectionJson[key].get(data).get('z_1')),
                                      yon=int(DataCollectionJson[key].get(data).get('tip', 3)),
                                      isim=DataCollectionJson[key].get(data).get('adı'), collection=collection,
                                      texture='mermerBeyaz', wallType=wallType)


def kutu_Olustur(self, DataCollectionJson, CollectionName='Yusuf'):
    collection = self.createNewCollection(CollectionName)
    for key in DataCollectionJson.keys():
        wallType = DataCollectionJson.get('duvar_no', '0')

        if type(DataCollectionJson[key]) is dict:
            topOfItem = list(DataCollectionJson[key].keys())
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
                                    isim=DataCollectionJson[key]['adı'], collection=collection, wallType=wallType)
                            else:
                                if DataCollectionJson[key].get('tip') == 3:
                                    genislik = DataCollectionJson[key].get('boy')
                                else:
                                    genislik = DataCollectionJson[key].get('en')

                                self.Obje_Olsutur(
                                    kalinlik=float(DataCollectionJson[key][dataName].get('kalınlık', 1.8)),
                                    derinlik=float(DataCollectionJson[key]['en']),
                                    yukseklik=float(DataCollectionJson[key].get('boy', 0)),
                                    modul_genislik=float(genislik),
                                    locationX=float(DataCollectionJson[key]['x_1']),
                                    locationY=float(DataCollectionJson[key]['y_1']),
                                    locationZ=float(DataCollectionJson[key]['z_1']),
                                    yon=int(DataCollectionJson[key].get('tip', 1)),
                                    isim=DataCollectionJson[key]['adı'], collection=collection, wallType=wallType)

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
                                    collection=collection, wallType=wallType)

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
                                        collection=collection, wallType=wallType)
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
                                        collection=collection, wallType=wallType)
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
                                        collection=collection, wallType=wallType)
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
                                        collection=collection, wallType=wallType)


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
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False)
    obj = bpy.context.scene.objects["Cube"]  # Get the object
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    bpy.context.view_layer.objects.active = obj
    obj.name = str(isim + '_' + str(yon) + '_' + str(randrange(100)))
    self.assignMaterial(texture, obj)

    if yon is 2:  # sağ_yan
        obj.dimensions = (derinlik, kalinlik, yukseklik)
        obj.location = (-(derinlik / 2), -(kalinlik / 2), -(yukseklik / 2))
    elif yon is 3:  # ust
        obj.dimensions = (derinlik, modul_genislik, kalinlik)
        obj.location = ((-derinlik / 2), (-modul_genislik / 2), (-kalinlik / 2))
    elif (yon is 1) or (yon is 4):  # kapak
        obj.dimensions = (kalinlik, modul_genislik, yukseklik)
        obj.location = (-(kalinlik / 2), -(modul_genislik / 2), -(yukseklik / 2))
    else:
        print('\n')

    if (locationX is not 0) or (locationY is not 0) or (locationZ is not 0):
        x, y, z = obj.location
        if yon is 1:
            obj.location = ((x - locationZ), (y - locationX), (z - locationY))
        elif yon is 3:
            obj.location = ((x - locationZ), (y - locationX), (z - locationY))
        else:
            obj.location = ((x - locationZ), (y - locationX), (z - locationY))

    sahnedeki_objeler.append(obj)
    collection.objects.link(obj)

    if int(wallType) == 1 and ('kapak' in obj.name):
        self.wall2.append(obj)
    elif int(wallType) == 0 and ('kapak' in obj.name):
        self.wall1.append(obj)
    return obj

def collection_move(self, x, y, z, collection_adi):
    objects_sahne = bpy.data.collections[collection_adi].objects

    for obj in objects_sahne:
        old_locationX, old_locationY, old_locationZ = obj.location
        obj.location = (float(old_locationX - z), float(old_locationY - x), float(old_locationZ - y))

def createNewCollection(self, CollectionName='Yusuf'):
    collection = bpy.data.collections.new(str(CollectionName))
    bpy.context.scene.collection.children.link(collection)
    return bpy.data.collections[CollectionName]


def assignMaterial(self, textureAdi='test', obj=bpy.context.active_object):
    obj.data.materials.append(bpy.data.materials[textureAdi])


def createNewScene(self):
    new_scene = bpy.data.scenes.new(name='DENEME')
    bpy.context.window.scene = new_scene


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