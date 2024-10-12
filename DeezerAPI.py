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


"""
Exemple pour id 13

{
    'data': [
        {
            'album': {
                'cover': 'https://api.deezer.com/album/119606/image',
                'cover_big': 'https://e-cdns-images.dzcdn.net/images/cover/e2b36a9fda865cb2e9ed1476b6291a7d/500x500-000000-80-0-0.jpg',
                'cover_medium': 'https://e-cdns-images.dzcdn.net/images/cover/e2b36a9fda865cb2e9ed1476b6291a7d/250x250-000000-80-0-0.jpg',
                'cover_small': 'https://e-cdns-images.dzcdn.net/images/cover/e2b36a9fda865cb2e9ed1476b6291a7d/56x56-000000-80-0-0.jpg',
                'cover_xl': 'https://e-cdns-images.dzcdn.net/images/cover/e2b36a9fda865cb2e9ed1476b6291a7d/1000x1000-000000-80-0-0.jpg',
                'id': 119606,
                'md5_image': 'e2b36a9fda865cb2e9ed1476b6291a7d',
                'title': 'Curtain Call: The Hits',
                'tracklist': 'https://api.deezer.com/album/119606/tracks',
                'type': 'album'
            },
            'artist': {
                'id': 13,
                'name': 'Eminem',
                'tracklist': 'https://api.deezer.com/artist/13/top?limit=50',
                'type': 'artist'
            },
            'contributors': [
                {
                    'id': 13,
                    'link': 'https://www.deezer.com/artist/13',
                    'name': 'Eminem',
                    'picture': 'https://api.deezer.com/artist/13/image',
                    'picture_big': 'https://e-cdns-images.dzcdn.net/images/artist/19cc38f9d69b352f718782e7a22f9c32/500x500-000000-80-0-0.jpg',
                    'picture_medium': 'https://e-cdns-images.dzcdn.net/images/artist/19cc38f9d69b352f718782e7a22f9c32/250x250-000000-80-0-0.jpg',
                    'picture_small': 'https://e-cdns-images.dzcdn.net/images/artist/19cc38f9d69b352f718782e7a22f9c32/56x56-000000-80-0-0.jpg',
                    'picture_xl': 'https://e-cdns-images.dzcdn.net/images/artist/19cc38f9d69b352f718782e7a22f9c32/1000x1000-000000-80-0-0.jpg',
                    'radio': True,
                    'role': 'Main',
                    'share': 'https://www.deezer.com/artist/13?utm_source=deezer&utm_content=artist-13&utm_term=0_1728744490&utm_medium=web',
                    'tracklist': 'https://api.deezer.com/artist/13/top?limit=50',
                    'type': 'artist'
                }
            ],
            'duration': 326,
            'explicit_content_cover': 0,
            'explicit_content_lyrics': 1,
            'explicit_lyrics': True,
            'id': 1109731,
            'link': 'https://www.deezer.com/track/1109731',
            'md5_image': 'e2b36a9fda865cb2e9ed1476b6291a7d',
            'preview': 'https://cdnt-preview.dzcdn.net/api/1/1/2/7/a/0/27a14827ff1e82c5e40e8b6a934a8637.mp3?hdnea=exp=1728745390~acl=/api/1/1/2/7/a/0...c5e40e8b6a934a8637.mp3*~data=user_id=0,application_id=42~hmac=f109783a93ede2d4ee7ae884e0c21b83e7b0d18f8510a19d27a3d74c9fece43a',
            'rank': 982936,
            'readable': True,
            'title': 'Lose Yourself',
            'title_short': 'Lose Yourself',
            'title_version': '',
            'type': 'track'
        }
    ],
    'next': 'https://api.deezer.com/artist/13/top?limit=1&index=1',
    'total': 100
}


"""




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