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
                # Récupère le premier titre dans les résultats
                title = data['data'][0]
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