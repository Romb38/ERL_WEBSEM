# Générateur de fichier turtle utilisant l'API de Deezer et de MusicBrainz

Ce projet à pour but de récupérer les informations de l'API de Deezer et de l'API de MusicBrainz pour les fusionner et créer un fichier Turtle.

#  Installation et prerequis
- Avoir DBGrapher
- Être connecté à internet
- Les dépendances python : ```python3 -m pip install requirements.txt```


# Structure du projet
 - **DeezerAPI.py** et **MusicBrainzAPI.py** recupère les informations sur les artistes,albums,musiques a partir d'API publique.
 - **adaptator.py** structure les informations de toutes les données pour le generateur de turtle. 
 - **tool.py** fonctions utilitaire pour le générateur
 - **main.py** Recuperation des données, formatage, écriture du fichier turtle.
 - **TurtleGenerator.py** Ecrit le turtle à partir des données (voir onthologie).
 - **requirement.txt** listes des librairie python necessaire.
 - **formatTurtle.sh** Suppression de certain caractere dans le turtle.

# Generation du turtle
- ```python3 main.py```

L'opération peut prendre plusieurs minutes du aux restrictions sur le nombre de requêtes sur les API.


# Requêtes SPARQL

Le résultat de toutes les requetes est stocké sous format json dans le dossier SQPARQL_response

 - Recupere toutes les musiques puis donne l'artiste et le vrai nom de l'artiste

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

 - Répertorie tous les artistes ayant composé au moins un album du genre "Rap/Hip Hop"
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

  - Compte le nombre d'album par genre (tri par ordre décroissant)
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

## Auteurs

Lucas SUBE
Elsa BOURGEOIS
Romain BARBIER