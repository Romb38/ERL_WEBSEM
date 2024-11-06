# Import the module
import musicbrainzngs

def set_usagent():
    # Tell musicbrainz what your app is, and how to contact you
    # (this step is required, as per the webservice access rules
    # at http://wiki.musicbrainz.org/XML_Web_Service/Rate_Limiting )
    musicbrainzngs.set_useragent("ERL_WEBSEM", "0.1")

def getDataFromArtistID(artist_id):
    try:
        result = musicbrainzngs.get_artist_by_id(artist_id, includes=["aliases"])
    #TODO : traiter exceptions correctement
    except Exception as exc:
        print("Something went wrong with the request: %s" % exc)
    else:
        artist = result["artist"]
        print("name:\t\t%s" % artist["name"])
        print("sort name:\t%s" % artist["sort-name"])
        return artist

def searchUSArtistByName(artist_name):
    #Strict true car sinon req sans fields assignés
    result = musicbrainzngs.search_artists(strict=True, artist="Eminem", country="US")

    for artist in result['artist-list']:
        print(u"{id}: {name}".format(id=artist['id'], name=artist['name']))

def getArtistLegalName(artist_id):
    try:
        result = musicbrainzngs.get_artist_by_id(artist_id, includes=['aliases'])

    except Exception as exc:
        print("Something went wrong with the request: %s" % exc)
    else:
        artist = result["artist"]
        for alias in artist['alias-list']:
            print(alias)
            if alias['type'] == 'Artist name' and alias['locale'] == 'en':
                print("Artist name (en):\t\t%s" % alias["alias"])
            elif alias['type'] == 'Legal name':
                print("Legal name:\t\t%s" % alias["alias"])
        return result
