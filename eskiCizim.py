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