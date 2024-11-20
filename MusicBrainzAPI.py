# Import the module
from time import sleep
import musicbrainzngs

def set_usagent():
    # Tell musicbrainz what your app is, and how to contact you
    # (this step is required, as per the webservice access rules
    # at http://wiki.musicbrainz.org/XML_Web_Service/Rate_Limiting )
    musicbrainzngs.set_useragent("ERL_WEBSEM", "0.1")

def getDataFromArtistID(artist_id):
    try:
        sleep(0.2)
        #Récupérer les artistes depuis leurs id en incluant leurs alias
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
    sleep(0.2)
    #Récupérer les artistes avec leur nom, qui sont aux US
    #Strict true car sinon req ne suite pas la demande
    result = musicbrainzngs.search_artists(strict=True, artist=artist_name, country="US")
    
    for artist in result['artist-list']:
        print(u"{id}: {name}".format(id=artist['id'], name=artist['name']))
    

def searchArtistByName(artist_name):
    sleep(0.2)
    #Récupérer le 1er artiste depuis son nom incluant ses alias
    #Strict true car sinon req ne suite pas la demande
    result = musicbrainzngs.search_artists(strict=True, limit=1, artist=artist_name, **{'alias':''})
    
    #Liste donc retourner l'élement 0
    if len(result['artist-list']) == 0:
        return None
    return result['artist-list'][0]

    #for artist in result['artist-list']:
    #    print(u"{id}: {name}".format(id=artist['id'], name=artist['name']))

def getArtistLegalNameById(artist_id):
    try:
        sleep(0.2)
        result = musicbrainzngs.get_artist_by_id(artist_id, includes=['aliases'])

    except Exception as exc:
        print("Something went wrong with the request: %s" % exc)
    else:
        artist = result["artist"]
        if (artist['type'] == 'Person'):
            for alias in artist['alias-list']:
                #if alias['type'] == 'Artist name' and ('locale' in alias and alias['locale'] == 'en'):
                #    print("Artist name (en):\t\t%s" % alias["alias"])
                if alias['type'] == 'Legal name':
                    legalName = alias["alias"]
                    print("Legal name:\t\t%s" % alias["alias"])
            return legalName
    
    
def getArtistLegalName(artist_name):
    artist = searchArtistByName(artist_name)
    if artist is None:
        return None
    locale_list = ['fr', 'fr_FR', 'en', 'en_US']
    legalName = None

    #Si groupe il n'y pas pas de nom légal
    if ('type' in artist and artist['type'] == 'Person') and ('alias-list' in artist):
        for alias in artist['alias-list']:
            if 'type' in alias and alias['type'] == 'Legal name' :
                
                #Cas où locale existe en plusieurs langues : garder seulement langues précisées
                #Cas où locale n'existe pas
                #renvoyer
                if ('locale' in alias and (alias['locale'] in locale_list)) or ('locale' not in alias):
                    legalName = [x.strip() for x in alias['sort-name'].split(',')]

    return legalName
    

