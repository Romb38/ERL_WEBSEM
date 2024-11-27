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



    IDsParams = getGenIDsParam(allInfos,featurings)
    artistParams = getGenArtistParams(allInfos,featurings)
    songsParam = getGenSongParam(allInfos)
    albumParams = getGenAlbumParam(allInfos)
    return IDsParams,artistParams,songsParam,albumParams


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
        ids.extend(list(info['tracks']))
    return ids

def getAllAlbumIDs(allInfos):
    ids = []
    for info in allInfos:
        ids.extend(list(info['album']))
    return ids

def getAllKind(allInfo):
    kinds = []
    for info in allInfo:
        album = info['album']
        for key,value in album.items():
            kind = value[1]
            if kind not in kinds:
                kinds.append(kind)

    kindsParsed = []
    for k in kinds:
        if k:
            kindsParsed.extend(k)
    kindsParsed.append("")
    return kindsParsed


def getGenIDsParam(allInfos, featurings):
    ARTIST_NAMES = getAllArtistNames(allInfos, featurings)
    SONG_IDS = getAllSongIDs(allInfos)
    ALBUM_IDS = getAllAlbumIDs(allInfos)
    KINDS = getAllKind(allInfos)
    return (ARTIST_NAMES, SONG_IDS, ALBUM_IDS, KINDS)

def getGenArtistParams(allInfos, featurings):
    #ARTIST_NAME,
    #artistName,
    #givenName,
    #familyName,
    #ALBUM_IDS,
    #SONG_IDS,
    artistParams = []
    for info in allInfos:
        artist_name = info['artist_name']
        given_name = info['given_name']
        family_name = info['family_name']
        album_ids = list(info['album'])
        tracks_ids = list(info['tracks'])
        artistParams.append((artist_name, given_name, family_name, album_ids, tracks_ids))

    for feat in featurings:
        #artist_id + artist_name + given_name + family_name
        #artist_id = feat[0]
        artist_name = feat[1]
        given_name = feat[2]
        family_name = feat[3]
        album_ids = []
        tracks_ids = []
        artistParams.append((artist_name, given_name, family_name, album_ids, tracks_ids))
    return artistParams

def getGenSongParam(allInfo):
    #SONG_ID,
    #ARTIST_NAME,
    #SONG_NAME,
    #FEATURED_ARTIST_NAMES
    songParams = []
    for info in allInfo:
        artist_name = info['artist_name']
        for key,value in info['tracks'].items():
            song_id = key
            song_name = value['track_name']
            featured_artist_names = value['featuring']
            songParams.append((song_id, artist_name, song_name, featured_artist_names))


    return songParams


def getGenAlbumParam(allInfos):
    #ALBUM_ID,
    #ALBUM_NAME,
    #ARTIST_NAME,
    #KIND,
    #SONGS_IDS
    albumParams = []
    #ID(clef) + (nom + list genre + list track_id)(tuples)
    for info in allInfos:
        artist_name = info['artist_name']
        for key, value in info['album'].items():
            album_id = key
            album_name = value[0]
            if value[1] != []:
                kind = value[1][0]
            else:
                kind = ""
            songs_ids = value[2]
            albumParams.append((album_id, album_name,artist_name, kind, songs_ids))

    return albumParams