import DeezerAPI as DAPI
import MusicBrainzAPI as MBAPI
import adaptator as adapt
import TurtleGenerator as gen

def main():
    MBAPI.set_usagent() # Pour pouvoir faire des appel à l'API de MusicBrainz
    #DAPI.getTitleFromArtistID(13)
    datas = []
    data = DAPI.getDataFromArtistID(13)
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


    #DAPI.generateTurtle(20)
    #Identification pour accéder à l'API MusicBrainz


    #MBAPI.getDataFromArtistID("db92a151-1ac2-438b-bc43-b82e149ddd50")
    #MBAPI.searchArtistByName("Eminem")
    #print(MBAPI.getArtistLegalName("eminem"))
    #MBAPI.getArtistLegalNameById("b95ce3ff-3d05-4e87-9e01-c97b66af13d4")
    return


if __name__ == '__main__':
    main()
