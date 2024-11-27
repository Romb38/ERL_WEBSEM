import DeezerAPI as DAPI
import MusicBrainzAPI as MBAPI
import adaptator as adapt
import TurtleGenerator as gen

def main():
    MBAPI.set_usagent() # Pour pouvoir faire des appel à l'API de MusicBrainz
    #DAPI.getTitleFromArtistID(13)
    datas = []
    for i in range(10):
        data = DAPI.getDataFromArtistID(744+i)
        if data['data'] == []:
            print(f"Aucune donnée pour l'artiste {744+i}")
            continue
        datas.append(data)

    #plus tard faire une boucle sur datas

    generator = gen.Generator("./turtle.ttl")
    idsParams,artistParams,songParams,albumParams = adapt.getFormatedData(datas)
    generator.genIDS(idsParams[0],idsParams[1],idsParams[2],idsParams[3])
    for artistParam in artistParams:
        generator.genArtist(artistParam[0],"",artistParam[1],artistParam[2],artistParam[3],artistParam[4])

    for songParam in songParams:
        generator.genSong(songParam[0],songParam[1],songParam[2],songParam[3])

    for albumParam in albumParams:
        generator.genAlbum(albumParam[0],albumParam[1],albumParam[2],albumParam[3],albumParam[4])

    for kinds in idsParams[3]:
        generator.genKind(kinds)


    return


if __name__ == '__main__':
    main()
