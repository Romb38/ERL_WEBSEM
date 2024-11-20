import DeezerAPI as DAPI
import MusicBrainzAPI as MBAPI

def main():
    #DAPI.getTitleFromArtistID(13)
    data = DAPI.getDataFromArtistID(13)
    print(DAPI.getAllInfoFromData(data))
    #tracks = DAPI.getAllTracksFromData(data)
    #print(tracks)

    #DAPI.generateTurtle(20)
    #Identification pour accéder à l'API MusicBrainz
    MBAPI.set_usagent()

    DAPI.getTitleFromArtistID(13)
    data = DAPI.getDataFromArtistID(13)
    tracks = DAPI.getAllTracksFromData(data)
    print(tracks)
    print("\n")
    
    #MBAPI.getDataFromArtistID("db92a151-1ac2-438b-bc43-b82e149ddd50")
    #MBAPI.searchArtistByName("Eminem")
    print(MBAPI.getArtistLegalName("georges brassens"))
    print(MBAPI.getArtistLegalName("eminem"))
    #MBAPI.getArtistLegalNameById("b95ce3ff-3d05-4e87-9e01-c97b66af13d4")
    return


if __name__ == '__main__':
    main()
