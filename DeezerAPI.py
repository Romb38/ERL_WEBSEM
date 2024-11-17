from time import sleep

import requests

BASE_URL = "https://api.deezer.com"

def getTitleFromArtistID(artist_id):
    """
    Get from Deezer API the first title of the artist
    :param artist_id: Integer - ID of the artist
    :return: JSON data which represent the title of the artist or None if it doesn't exist
    """
    # URL de l'API Deezer pour récupérer le top titre de l'artiste
    url = f"{BASE_URL}/artist/{artist_id}/top"

    try:
        # Effectue la requête GET
        response = requests.get(url)

        # Vérifie que la requête a réussi
        if response.status_code == 200:
            # Parse la réponse en JSON
            data = response.json()

            # Vérifie s'il y a des données
            if 'data' in data and len(data['data']) > 0:
                # Récupère le premier titre dans les résultats
                track = data['data'][0]
                title = track['title']
                id_track = track['id']
                artist = track['artist']['name']

                print(f"title: {title}")
                print(f"id_track: {id_track}")
                print(f"artist: {artist}")

                return title
            else:
                return None
        else:
            return f"Erreur {response.status_code} lors de la requête."

    except Exception as e:
        return f"Une erreur est survenue : {str(e)}"






def getArtistIDByName(artist_name):
    """
    Return the ID of the artist from its name
    :param artist_name: String - Name of the artist
    :return: Integer - ID of the artist or -1 if it doesn't exist
    """
    # URL de l'API Deezer pour rechercher l'artiste par son nom
    url = f"{BASE_URL}/search/artist?q={artist_name}"

    try:
        # Effectue la requête GET
        response = requests.get(url)

        # Vérifie que la requête a réussi
        if response.status_code == 200:
            # Parse la réponse en JSON
            data = response.json()

            # Vérifie s'il y a des résultats
            if 'data' in data and len(data['data']) > 0:
                # Récupère l'ID du premier artiste dans les résultats
                artist_id = data['data'][0]['id']
                return artist_id
            else:
                return -1
        else:
            return f"Erreur {response.status_code} lors de la requête."

    except Exception as e:
        return f"Une erreur est survenue : {str(e)}"



def getTitleFromIncreasingArtistId(nb_title, base_artist_id=1):
    """
    Get from Deezer API the first title of nb_title artist without triggering request limit
    It serach by increasing the base id of 1 each loop
    :param nb_title: Number of title you want in the list
    :param base_artist_id: Integer - Beginning id of the artist list
    :return: List of json title
    """
    out = []
    for i in range(base_artist_id, base_artist_id+nb_title):
        title = getTitleFromArtistID(i)
        if title :
            out.append(title)
        sleep(0.2)


    return out




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


def getAllTracksFromData(data):
    """
    Get an array of tracks name from data fetched from Deeze API
    :param data: Dictionnary - data of the artist
    :return: array of tracks name from the artist
    """
    artist_id = data['data'][0]['artist']['id']

    # Récupère les 5000 premières pistes de l'artiste
    tracks = {}
    try:
        url = f"{BASE_URL}/artist/{artist_id}/top?limit=5000"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                # Extrait les titres des pistes
                for track in data['data']:
                    track_name = track['title']
                    featured_artists = []
                    for artist in track['contributors']:
                        #if artist['role'] == "Featured":
                        featured_artists.append(artist['name'])
                    tracks[track_name] = featured_artists

                return tracks
            else:
                return None


    except Exception as e:
        return f"Une erreur est survenue : {str(e)}"




def getArtistByData(data):
    return data['data'][0]["artist"]["name"]



def writePrefix():
    with open("turtle.ttl", "w") as turtle:
        turtle.write("@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n")
        turtle.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
        turtle.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .  \n")
        turtle.write("@prefix dbr: <https://dbpedia.org/resource#> .\n")
        turtle.write("@prefix mo: <http://purl.org/ontology/mo/> .\n")
        turtle.write("\n\n")


def parsing(toparse):
    return toparse.replace(" ", "_")


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
        allInfo['album'] = {} # ID(clef) + (nom + genre + list track_id)(tuples)
        allInfo['given_name'] = "Jean" # Todo
        allInfo['family_name'] = "Michel" # Todo

        featuring = {} # artist_id + artist_name + given_name + family_name


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
                        allInfo['tracks'][track_id]['featuring'] = featured_artists

                        # ALBUM
                        album = track['album']
                        album_id = album['id']
                        if album_id not in allInfo['album']:
                            allInfo['album'][album_id] = (
                                album['title'],
                                getGenreFromAlbumId(album_id),  # Fait une requete donc contient un sleep pour pas surcharger api
                                []
                            )
                        allInfo['album'][album_id][2].append(track_id)


                    return allInfo,featuring
                else:
                    return None
            else:
                return f"Une erreur est survenue"
        except Exception as e:
            print(f"Error : {e}")

def generateTurtle(n):
    writePrefix()
    artists = {}
    #Todo changer en un while pour faire +1 en cas de data == None
    for i in range(n):
        data = getDataFromArtistID(i+1)
        if data != None:
            artist_name = parsing(getArtistByData(data))
            tracks = getAllTracksFromData(data)
            artists[artist_name] = tracks
        sleep(0.5)



    with open("turtle.ttl", "a") as turtle:
        for artist in artists.keys():
            turtle.write(f"erl:{artist} a foaf:Person ;\n")
            turtle.write(f"\tfoaf:givenName \"Jean\" ;\n")
            turtle.write(f"\tfoaf:familyName \"Michel\" ;\n")
            turtle.write(f"owl : sameAs dbr :{artist} .")
            # Point sur la fin
            turtle.write("\n\n")

        # Todo travail en cours (Lucas)

        """for track in artists.values():
            i = 0
            # todo : Faire un meilleur ID de track (hashing ?)
            turtle.write(f"erl:{track.keys()[i]} a dbo:Song ;\n")
            turtle.write(f"\tfoaf:person  erl:\"ID DE L'ARTIST'\" ;\n")
            turtle.write(f"\tdbo : featuredArtist erl :{ ID_Featured_Artist }\n")
            # Point sur la fin
            turtle.write("\n\n")
        """





