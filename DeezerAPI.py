from time import sleep
from MusicBrainzAPI import getArtistLegalName
import requests

BASE_URL = "https://api.deezer.com"



def getDataFromArtistID(artist_id):
    """
    Get from Deezer API the data of the artist
    :param artist_id: Integer - ID of the artist
    :return: JSON data which represent the title of the artist or None if it doesn't exist
    """
    url = f"{BASE_URL}/artist/{artist_id}/top?limit=1"
    try:
        # Effectue la requête GET
        response = requests.get(url)
        # Vérifie que la requête a réussi
        if response.status_code == 200:
            # Parse la réponse en JSON
            data = response.json()
            # Vérifie s'il y a des données
            if 'data' in data and len(data['data']) > 0:
                return data
            else:
                return None
        else:
            return f"Erreur {response.status_code} lors de la requête."

    except Exception as e:
        return f"Une erreur est survenue : {str(e)}"






def getGenreFromAlbumId(album_id):
    """
    Get from Deezer API the genre of the album
    :param album_id: Integer - ID of the album
    :return: String - Genre of the album
    """
    try:
        sleep(0.2)
        url = f"{BASE_URL}/album/{album_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            genresString = []
            for genre in data['genres']['data']:
                genresString.append(genre['name'])
            return genresString
        else:
            return f"Erreur {response.status_code} lors de la requête."
    except Exception as e:
        print(f"Error : {e}")





def getAllInfoFromData(data):
        """
        artist_id = id d'artiste a générer
        artist_name = nom d'artiste
        liste de toute ses musique -> id + nom + featuring
        liste de tout ses album -> ID + Nom + genre + liste des musique
        givenName = Vrai nom (plus tard)
        Vrai prénom (plus tard)

        """
        allInfo = {}
        allInfo['artist_id'] = data['data'][0]['id'] # Généré plus tard
        allInfo['artist_name'] = data['data'][0]['artist']['name']  # nom d'artiste
        allInfo['tracks'] = {} # track_id(clef) + (track_name + featuring)(tuples) #Todo ajouté info artiste
        allInfo['album'] = {} # ID(clef) + (nom + list genre + list track_id)(tuples)

        realName = getArtistLegalName(allInfo['artist_name'])
        if (realName != None and len(realName) > 1):
            allInfo['given_name'] = realName[0]
            allInfo['family_name'] = realName[1]
        else:
            allInfo['given_name'] = ""
            allInfo['family_name'] = ""

        featuring = [] #  artist_name[]
        featuringTuple = [] # (artist_id + artist_name + given_name + family_name)

        deezer_artist_id = data['data'][0]['artist']['id']


        # Récupère les 5000 premières pistes de l'artiste
        try:
            sleep(0.2)
            url = f"{BASE_URL}/artist/{deezer_artist_id}/top?limit=5000"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:

                    # TRACKS
                    for track in data['data']:
                        track_id = track['id']
                        allInfo['tracks'][track_id] = {
                            'track_name': track['title'],
                            'featuring': []
                        }

                        # FEATURING
                        featured_artists = []
                        for artist in track['contributors']:
                            if artist['role'] == "Featured":
                                # Todo pour l'instant juste les noms
                                featured_artists.append(artist['name'])
                                if artist['name'] not in featuring:
                                    featuring.append((artist['name'],artist['id']))
                        allInfo['tracks'][track_id]['featuring'] = featured_artists

                        # ALBUM
                        album = track['album']
                        album_id = album['id']
                        if album_id not in allInfo['album']:
                            allInfo['album'][album_id] = (
                                album['title'],
                                getGenreFromAlbumId(album_id),  # Fait une requete donc contient un sleep pour pas surcharger api
                                []          #Ne pas déplacer l'ordre dans la structure
                            )
                        allInfo['album'][album_id][2].append(track_id)


                    # REAL NAMES OF FEATURING ARTIST
                    for artist in featuring:
                        print(f"Get real name of {artist[0]}")
                        realName = getArtistLegalName(artist[0])
                        if realName!= None and len(realName) <2 :
                            realName = None
                        if realName!= None:
                            featuringTuple.append((artist[1],artist[0],realName[0],realName[1]))
                        else:
                            featuringTuple.append((artist[1],artist[0],"",""))
                    return allInfo,featuringTuple
                else:
                    return None
            else:
                return f"Une erreur est survenue"
        except Exception as e:
            print(f"Error : {e}")


