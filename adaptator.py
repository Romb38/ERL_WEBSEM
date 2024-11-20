from DeezerAPI import getAllInfoFromData





def getFormatedData(datas):
    allInfos = []
    featurings = []
    for data in datas:
        print("Get new data")
        inf,fea = getAllInfoFromData(data)
        allInfos.append(inf)
        featurings.extend(fea)

    print("End of getting data")


    ARTIST_NAMES = getAllArtistNames(allInfos,featurings)
    SONG_IDS = getAllSongIDs(allInfos)
    ALBUM_IDS = getAllAlbumIDs(allInfos)
    KINDS = getAllKind(allInfos)
    return ARTIST_NAMES,SONG_IDS,ALBUM_IDS,KINDS


def getAllArtistNames(allInfos, featurings):
    names = []
    for info in allInfos:
        names.append(info['artist_name'])

    for feat in featurings:
        names.append(feat[1])
    return names

def getAllSongIDs(allInfos):
    ids = []
    for info in allInfos:
        ids.append(list(info['tracks']))
    return ids

def getAllAlbumIDs(allInfos):
    ids = []
    for info in allInfos:
        ids.append(list(info['album']))
    return ids

def getAllKind(allInfo):
    kinds = []
    for info in allInfo:
        album = info['album']
        for key,value in album.items():
            kind = value[1]
            if kind not in kinds:
                kinds.append(kind)
    return kinds
