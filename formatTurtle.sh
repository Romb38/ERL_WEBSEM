#!/bin/bash

# Vérifie si un fichier a été fourni en paramètre
if [ $# -eq 0 ]; then
  echo "Usage: $0 <nom_du_fichier>"
  exit 1
fi

# Récupère le nom du fichier depuis le premier paramètre
fichier="$1"

# Vérifie si le fichier existe
if [ ! -f "$fichier" ]; then
  echo "Erreur : le fichier '$fichier' n'existe pas."
  exit 1
fi

# Supprime les caractères '\' du fichier
perl -i -pe 's/\\(?!")//g' $fichier






echo "Les caractères '\\' ont été supprimés du fichier '$fichier'."