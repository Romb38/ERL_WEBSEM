import DeezerAPI as DAPI

def main():
    #DAPI.getTitleFromArtistID(13)
    data = DAPI.getDataFromArtistID(13)
    print(DAPI.getAllInfoFromData(data))
    #tracks = DAPI.getAllTracksFromData(data)
    #print(tracks)

    #DAPI.generateTurtle(20)
    return


if __name__ == '__main__':
    main()