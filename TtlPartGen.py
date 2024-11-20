import tools


def genIDS(
        ARTIST_NAMES,
        SONG_IDS,
        ALBUM_IDS,
        KINDS
):
    """
    Génère la totalité des IDs interne des différentes données

    @param ARTIST_IDS Liste des noms de tous les artistes
    @param SONG_IDS Liste des IDs de Deezer de toutes les chansons (tout artistes confondus)
    @param ALBUM_IDS Liste des IDs de Deezer de tous les albums (tout artistes confondu)
    @param KIND Liste de tous les nom de genre de Deezer (tout artistes confondu)
    
    """
    for ARTIST_NAME in ARTIST_NAMES :
        ID_Artist_Name = tools.formatLine(ARTIST_NAME)
        tools.ARTIST_LINK[ARTIST_NAME] = ID_Artist_Name
    
    for SONG_ID in SONG_IDS:
        UUID_SONG = tools.getUUID()
        tools.SONG_LINK[SONG_ID] = UUID_SONG
    
    for ALBUM_ID in ALBUM_IDS :
        UUID_ALBUM = tools.getUUID()
        tools.ALBUM_LINK[ALBUM_ID] = UUID_ALBUM
    
    for KIND in KINDS :
        KIND_LABEL = tools.formatLine(KIND)
        tools.KIND_LINK[KIND] = KIND_LABEL 

def genPrefix() :
    """
    Créer la liste des namespaces nécessaire au projet

    @return String - Liste des namespaces
    """

    return """
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dbo: <http://dbpedia.org/ontology/> .
    @prefix dbr: <http://dbpedia.org/resource/> .
    @prefix owl: <http://www.w3.org/2002/07/owl#>/ .
    @prefix erl: <http://www.websem.csv/resource/> .
    @prefix erlo: <http://www.websem.csv/ontology/> .
    """

def genArtist(
        ARTIST_NAME,
        artistName,
        givenName,
        familyName,
        ALBUM_IDS,
        SONG_IDS,
):
    """
    Génère un objet Artiste en turtle

    @param ARTIST_NAME Nom de l'artiste selon Deezer
    @param artistName Alias de l'artiste
    @param givenName Prénom de l'artiste
    @param familyName Nom de famille de l'artiste
    @param ALBUMS_IDS Liste des IDs de Deezer des albums produits par l'artiste
    @param SONG_IDs Liste des IDs de Deezer des chansons composée par l'artiste
    
    @return String - Objet Artiste en turtle
    """
    ID_Artist_Name = tools.ARTIST_LINK[ARTIST_NAME]
    ALBUMS = "\n".join(f"erlo:produce erl:{tools.ALBUM_LINK[ALBUM_ID]} ;" for ALBUM_ID in ALBUM_IDS)
    SONG = "\n".join(f"erlo:compose erl:{tools.SONG_LINK[SONG_ID]} ;" for SONG_ID in SONG_IDS)
    
    if givenName : 
        GIVEN_NAME = "foaf:givenName \"{givenName}\" ;\n"
    else :
        GIVEN_NAME = ""

    if familyName : 
        FAMILY_NAME = "foaf:familyName \"{familyName}\" ;\n"
    else :
        FAMILY_NAME = ""

    return f"""
    erl:{ID_Artist_Name} a foaf:Person
        dbo:artist dbr:{ID_Artist_Name} ;
        {GIVEN_NAME}
        {FAMILY_NAME}
        dbo:alias "{artistName}" ;
        owl:sameAs dbr:{ID_Artist_Name} ;
        {ALBUMS}
        {SONG[:-2]} .
        .
    """

def genSong(
    SONG_ID,
    ID_ARTIST_NAME,
    SONG_NAME,
    FEATURED_ARTIST_NAMES
):
    """
    Génére un objet Chanson en turtle

    @param SONG_ID ID de Deezer de la chanson
    @param ID_ARTIST_NAME Nom de l'artiste qui à composé la chanson
    @param SONG_NAME Nom de la chanson
    @param FEATURED_ARTIST_NAMES Liste de noms des artistes en featuring sur la chanson

    @return String - Objet Chanson en turtle
    """
    UUID_SONG = tools.SONG_LINK[SONG_ID]
    if (len(FEATURED_ARTIST_NAMES) > 0) :
        FEATURED_ARTIST = "\n".join(f"dbo:featuredArtist erl:{tools.ARTIST_LINK[FEATURED_ARTIST_NAME]} ;" for FEATURED_ARTIST_NAME in FEATURED_ARTIST_NAMES)
    else : 
        FEATURED_ARTIST = ""


    return f"""
    erl:{UUID_SONG} a dbo:Song
        foaf:Person erl:{ID_ARTIST_NAME} ;
        rdfs:label "{SONG_NAME}" ;
        {FEATURED_ARTIST[:-2]} .
    .
    """

def genAlbum(
        ALBUM_ID,
        ALBUM_NAME,
        ARTIST_NAME,
        KIND,
        SONGS_IDS
):
    """
    Créer un objet Album en turtle

    @param ALBUM_ID ID selon Deezer de l'album
    @param ALBUM_NAME Nom de l'album
    @param ARTIST_NAME Nom de l'artiste qui à conçu l'album
    @param KIND Genre de l'album selon Deezer
    @param SONGS Liste des IDs selon Deezer des chansons de l'album

    @return String - Objet Album en turtle
    """
    UUID_ALBUM = tools.ALBUM_LINK[ALBUM_ID]
    ID_ARTIST_NAME = tools.ARTIST_LINK[ARTIST_NAME]
    KIND_LABEL = tools.KIND_LINK[KIND]
    SONGS = "\n".join(f"erlo:contains erl:{tools.SONG_LINK[SONG_ID]} ;" for SONG_ID in SONGS_IDS)
    return f"""
    erl:{UUID_ALBUM} a dbo:Album
        rdfs:label "{ALBUM_NAME}" ;
        foaf:Person erl:{ID_ARTIST_NAME} ;
        dbo:genre erl:{KIND_LABEL} ;
        {SONGS[:-2]} .
    """

def genKind(
    KIND,
):
    """
    Créer un objet Genre en turtle

    @param KIND Nom du genre

    @return String - Objet Genre en turtle
    """
    KIND_LABEL = tools.KIND_LINK[KIND]
    return f"""
    erl:{KIND_LABEL} a dbo:genre
        rdfs:label "{KIND}" ;
        owl:sameAs "{KIND_LABEL}" .
    """