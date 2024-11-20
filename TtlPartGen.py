import tools

def genPrefix() :
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
        artistName,
        givenName,
        familyName,
        UUID_ALBUMS,
        UUID_SONGS,
):
    ID_Artist_Name = tools.formatLine(artistName)
    ALBUMS = "\n".join(f"erlo:produce erl:{UUID_ALBUM} ;" for UUID_ALBUM in UUID_ALBUMS)
    SONG = "\n".join(f"erlo:compose erl:{UUID_SONG} ;" for UUID_SONG in UUID_SONGS)

    return (ID_Artist_Name, f"""
    erl:{ID_Artist_Name} a foaf:Person
        dbo:artist dbr:{ID_Artist_Name} ;
        foaf:givenName "{givenName}" ;
        foaf:familyName "{familyName}" ;
        dbo:alias "{artistName}" ;
        owl:sameAs dbr:{ID_Artist_Name} ;
        {ALBUMS}
        {SONG}
        .
    """)

def genSong(
    ID_ARTIST_NAME,
    SONG_NAME,
    IDS_FEATURED_ARTIST
):
    UUID_SONG = tools.getUUID()
    FEATURED_ARTIST = "\n".join(f"dbo:featuredArtist erl:{ID_FEATURED_ARTIST} ;" for ID_FEATURED_ARTIST in IDS_FEATURED_ARTIST)

    return (UUID_SONG, f"""
    erl:{UUID_SONG} a dbo:Song
        foaf:Person erl:{ID_ARTIST_NAME} ;
        rdfs:label "{SONG_NAME}" ;
        dbo:Album erl:IDAlbum ;
        {FEATURED_ARTIST}
    .
    """)

def genAlbum():
    pass

def genKind(
    KIND,
):
    KIND_LABEL = tools.formatLine(KIND)

    return (KIND_LABEL, f"""
    erl:{KIND_LABEL} a dbo:genre
        rdfs:label "{KIND}" ;
        owl:sameAs "{KIND_LABEL}" .
    """)