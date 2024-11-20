import DeezerAPI as DAPI
import MusicBrainzAPI as MBAPI
import adaptator as adapt
import TurtleGenerator as gen

def main():
    MBAPI.set_usagent() # Pour pouvoir faire des appel à l'API de MusicBrainz
    #DAPI.getTitleFromArtistID(13)
    print(MBAPI.getArtistLegalName('Anthony Santos'))
    datas = []
    data = DAPI.getDataFromArtistID(700)
    #print(DAPI.getAllInfoFromData(data))
    datas.append(data)
    generator = gen.Generator
    ARTIST_NAMES, SONG_IDS, ALBUM_IDS, KINDS = adapt.getFormatedData(datas)
    generator.genIDS(ARTIST_NAMES, SONG_IDS, ALBUM_IDS, KINDS)

    #DAPI.generateTurtle(20)
    #Identification pour accéder à l'API MusicBrainz


    #MBAPI.getDataFromArtistID("db92a151-1ac2-438b-bc43-b82e149ddd50")
    #MBAPI.searchArtistByName("Eminem")
    #print(MBAPI.getArtistLegalName("eminem"))
    #MBAPI.getArtistLegalNameById("b95ce3ff-3d05-4e87-9e01-c97b66af13d4")
    return


if __name__ == '__main__':
    main()
