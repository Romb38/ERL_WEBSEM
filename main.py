import DeezerAPI as DAPI

def main():
    #DAPI.getTitleFromArtistID(13)
    data = DAPI.getDataFromArtistID(13)
    tracks = DAPI.getAllTracksFromData(data)
    print(tracks)

    DAPI.generateTurtle(20)
    return


if __name__ == '__main__':
    main()