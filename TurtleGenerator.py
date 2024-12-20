import tools
import os

class Generator:
    def __init__(self, file_path) -> None:
        """
        Générateur du fichier Turtle

        @param file_path Indique le chemin du fichier à écrire
        """

        self.path = file_path

        self.ARTIST_LINK = {}
        self.WRITTEN_ARTIST = []

        self.ALBUM_LINK = {}
        self.WRITTEN_ALBUM = []

        self.SONG_LINK = {}
        self.WRITTEN_SONG = []

        self.KIND_LINK = {}
        self.WRITTEN_KIND = []

        self.hadGenId = False

        if os.path.exists(self.path):
            os.remove(self.path)

        self.genPrefix()

    def write(self, content: str) -> None:
        # Supprimer les lignes vides
        non_empty_lines = "\n".join(line for line in content.splitlines() if line.strip())
        # Écrire dans le fichier
        with open(self.path, 'a') as f:
            f.write(non_empty_lines + "\n\n")

    def genIDS(
        self,
        ARTIST_NAMES : list[str],
        SONG_IDS : list[str],
        ALBUM_IDS : list[str],
        KINDS : list[str],
    ) -> None:
        """
        Génère la totalité des IDs interne des différentes données

        @param ARTIST_NAMES Liste des noms de tous les artistes
        @param SONG_IDS Liste des IDs de Deezer de toutes les chansons (tout artistes confondus)
        @param ALBUM_IDS Liste des IDs de Deezer de tous les albums (tout artistes confondu)
        @param KINDS Liste de tous les nom de genre de Deezer (tout artistes confondu)
        """
        for ARTIST_NAME in ARTIST_NAMES :
            ID_Artist_Name = tools.formatLine(ARTIST_NAME)
            self.ARTIST_LINK[ARTIST_NAME] = ID_Artist_Name
        
        for SONG_ID in SONG_IDS:
            UUID_SONG = tools.getUUID()
            self.SONG_LINK[SONG_ID] = UUID_SONG
        
        for ALBUM_ID in ALBUM_IDS :
            UUID_ALBUM = tools.getUUID()
            self.ALBUM_LINK[ALBUM_ID] = UUID_ALBUM
        
        for KIND in KINDS :
            KIND_LABEL = tools.formatLine(KIND)
            self.KIND_LINK[KIND] = KIND_LABEL

        self.hadGenId = True

    def genPrefix(self) -> None :
        """
        Créer la liste des namespaces nécessaire au projet
        """

        return self.write("""
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix erl: <http://www.websem.csv/resource/> .
@prefix erlo: <http://www.websem.csv/ontology/> .
        """)

    def genArtist(
            self,
            ARTIST_NAME : str,
            artistName : str,
            givenName : str,
            familyName : str,
            ALBUM_IDS : list[str],
            SONG_IDS : list[str],
    ) -> None:
        """
        Génère un objet Artiste en turtle

        @param ARTIST_NAME Nom de l'artiste selon Deezer
        @param artistName Alias de l'artiste
        @param givenName Prénom de l'artiste
        @param familyName Nom de famille de l'artiste
        @param ALBUM_IDS Liste des IDs de Deezer des albums produits par l'artiste
        @param SONG_IDS Liste des IDs de Deezer des chansons composée par l'artiste
        """

        if not(self.hadGenId):
            raise IDNotGenerated()

        ID_Artist_Name = self.ARTIST_LINK[ARTIST_NAME]

        # On vérifie que l'on à pas déjà écrit l'artiste
        if ID_Artist_Name in self.WRITTEN_ARTIST:
            return
        else :
            self.WRITTEN_ARTIST.append(ID_Artist_Name)

        # Si ALBUM_IDS ou SONG_IDS sont vide, alors la chaine résultante sera vide
        ALBUMS = "".join(f"erlo:produce erl:{self.ALBUM_LINK[ALBUM_ID]} ;\n\t" for ALBUM_ID in ALBUM_IDS)
        SONG = "".join(f"erlo:compose erl:{self.SONG_LINK[SONG_ID]} ;\n\t" for SONG_ID in SONG_IDS)


        if givenName : 
            GIVEN_NAME = f"foaf:givenName \"{tools.esc(givenName)}\" ;\n"
        else :
            GIVEN_NAME = ""

        if familyName : 
            FAMILY_NAME = f"foaf:familyName \"{tools.esc(familyName)}\" ;\n"
        else :
            FAMILY_NAME = ""

        if artistName :
            ALIAS_ARTIST = f"dbo:alias \"{artistName}\" ;"
        else :
            ALIAS_ARTIST = ""


        return self.write(f"""
erl:{ID_Artist_Name} a foaf:Person ;
    dbo:artist dbr:{ID_Artist_Name} ;
    {GIVEN_NAME}
    {FAMILY_NAME}
    {ALIAS_ARTIST}
    owl:sameAs dbr:{ID_Artist_Name} ;
    {ALBUMS[:-2]}
    {SONG[:-4]} .
        """)

    def genSong(
        self,
        SONG_ID : str,
        ARTIST_NAME : str,
        SONG_NAME : str,
        FEATURED_ARTIST_NAMES : list[str],
    ) -> None:
        """
        Génére un objet Chanson en turtle

        @param SONG_ID ID de Deezer de la chanson
        @param ARTIST_NAME Nom de l'artiste qui à composé la chanson
        @param SONG_NAME Nom de la chanson
        @param FEATURED_ARTIST_NAMES Liste de noms des artistes en featuring sur la chanson
        """
        if not(self.hadGenId):
            raise IDNotGenerated()

        UUID_SONG = self.SONG_LINK[SONG_ID]

        if UUID_SONG in self.WRITTEN_SONG:
            return
        else:
            self.WRITTEN_SONG.append(UUID_SONG)

        ID_ARTIST_NAME = self.ARTIST_LINK[ARTIST_NAME]

        if (len(FEATURED_ARTIST_NAMES) > 0) :
            FEATURED_ARTIST = "".join(f"dbo:featuredArtist erl:{self.ARTIST_LINK[FEATURED_ARTIST_NAME]} ;\n\t" for FEATURED_ARTIST_NAME in FEATURED_ARTIST_NAMES)
        else : 
            FEATURED_ARTIST = ""


        return self.write(f"""
erl:{UUID_SONG} a dbo:Song ;
    foaf:Person erl:{ID_ARTIST_NAME} ;
    rdfs:label "{tools.esc(SONG_NAME)}" ;
    {FEATURED_ARTIST[:-3]} .
        """)

    def genAlbum(
            self,
            ALBUM_ID : str,
            ALBUM_NAME : str,
            ARTIST_NAME : str,
            KIND : str,
            SONGS_IDS : list[str]
    ) -> None:
        """
        Créer un objet Album en turtle

        @param ALBUM_ID ID selon Deezer de l'album
        @param ALBUM_NAME Nom de l'album
        @param ARTIST_NAME Nom de l'artiste qui à conçu l'album
        @param KIND Genre de l'album selon Deezer
        @param SONGS_IDS Liste des IDs selon Deezer des chansons de l'album
        """

        if not(self.hadGenId):
            raise IDNotGenerated()

        UUID_ALBUM = self.ALBUM_LINK[ALBUM_ID]

        if UUID_ALBUM in self.WRITTEN_ALBUM:
            return
        else :
            self.WRITTEN_ALBUM.append(UUID_ALBUM)

        ID_ARTIST_NAME = self.ARTIST_LINK[ARTIST_NAME]
        KIND_LABEL = self.KIND_LINK[KIND]
        SONGS = "".join(f"erlo:contains erl:{self.SONG_LINK[SONG_ID]} ;\n\t" for SONG_ID in SONGS_IDS)
        
        return self.write(f"""
erl:{UUID_ALBUM} a dbo:Album ;
    rdfs:label "{tools.esc(ALBUM_NAME)}" ;
    foaf:Person erl:{ID_ARTIST_NAME} ;
    dbo:genre erl:{KIND_LABEL} ;
    {SONGS[:-3]} .
        """)

    def genKind(
        self,
        KIND : str,
    ) -> None:
        """
        Créer un objet Genre en turtle

        @param KIND Nom du genre
        """

        if not(self.hadGenId):
            raise IDNotGenerated()

        KIND_LABEL = self.KIND_LINK[KIND]
        if KIND_LABEL in self.WRITTEN_KIND:
            return
        else :
            self.WRITTEN_KIND.append(KIND_LABEL)

        return self.write(f"""
erl:{KIND_LABEL} a dbo:genre ;
    rdfs:label "{tools.esc(KIND)}" ;
    owl:sameAs "{KIND_LABEL}" .
        """)
    
class IDNotGenerated(Exception):
    def __init__(self, message="ID n'a pas été généré avant d'écrire."):
        self.message = message
        super().__init__(self.message)
