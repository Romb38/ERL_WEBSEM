# Générateur de fichier turtle utilisant l'API de Deezer et de MusicBrainz

Ce projet à pour but de récupérer les informations de l'API de Deezer et de l'API de MusicBrainz pour les fusionner et créer un fichier Turtle.

#  Installation et prerequis
- Être connecté à internet
- Installer les dépendances python : ```python3 -m pip install requirements.txt```

# Generation du turtle
- ```python3 main.py```

Cet algorithme génère un fichier turtle à partir des donées de Deezer et MusicBrainz. Pour cela, il prends les 100 premières IDs (de deezer) des chanteurs afin de récupérer leurs infos.
L'opération peut prendre plusieurs minutes du aux restrictions sur le nombre de requêtes sur les API.
Une fois cette opération terminée, on peut retrouver le fichier turtle ici : './turtle.ttl'

# Structure du projet
- **main.py** : Recuperation des données, formatage, écriture du fichier turtle.
- **DeezerAPI.py** et **MusicBrainzAPI.py** : recupère les informations sur les artistes,albums,musiques a partir d'API publique.
- **adaptator.py** : structure les informations de toutes les données pour le generateur de turtle. 
- **tool.py** : fonctions utilitaire pour le générateur
- **TurtleGenerator.py** : Ecrit le turtle à partir des données (voir onthologie).
- **formatTurtle.sh** : suppression de caractères d'échappement dans le fichier turtle.


# Requêtes SPARQL

Tous les résultats des requêtes sont stockées (sous format json) dans le dossier SQPARQL_response

 - **allSongs.srj** : Recupere toutes les musiques puis donne l'artiste et le vrai nom de l'artiste

```sql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX erl: <http://www.websem.csv/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?song ?songName ?artist ?givenName ?familyName
WHERE {
  ?song a dbo:Song ;
        rdfs:label ?songName ;
        foaf:Person ?artist .
  ?artist foaf:givenName ?givenName ;
    foaf:familyName ?familyName .
}
```

 -  **artistGenre.srj** : Répertorie tous les artistes ayant composé au moins un album du genre "Rap/Hip Hop"
```sql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX erl: <http://www.websem.csv/resource/>
PREFIX erlo: <http://www.websem.csv/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?artist
WHERE {
  ?artist a foaf:Person ;
          erlo:produce ?album .
  ?album a dbo:Album ;
        dbo:genre ?genre .
  ?genre rdfs:label "Rap/Hip Hop" .
}
```

  -  **genreCount.srj** : Compte le nombre d'album par genre (tri par ordre décroissant)

```sql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX erl: <http://www.websem.csv/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?genreLabel (COUNT(?album) AS ?albumCount)
WHERE {
  ?album a dbo:Album ;
         dbo:genre ?genre .
  ?genre rdfs:label ?genreLabel .
}
GROUP BY ?genreLabel
ORDER BY DESC(?albumCount)
```

  -  **albumList.srj** : Liste les albums d'Indochine et leur genre
  
```sql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX erlo: <http://www.websem.csv/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?albumName ?genre
WHERE {
  ?artist a foaf:Person ;
    dbo:artist dbr:Indochine;
          erlo:produce ?album .
  ?album a dbo:Album  ;
    rdfs:label ?albumName ;
    dbo:genre ?genre.
}
```

## Auteurs

Lucas SUBE
Elsa BOURGEOIS
Romain BARBIER