import shortuuid
import re

def getUUID() -> str:
    """
    Créé un nouvel ID unique
    :return: Chaine de caractère avec un identifiant unique
    """
    su = shortuuid.ShortUUID(alphabet="1234567890")
    return su.random(length=8)

def formatLine(input_string :str) -> str :
    """
    Transforme une chaîne en un identifiant CamelCase avec des underscores (_) entre les mots.

    @param input_string: La chaîne à convertir.
    @return: Une chaîne en CamelCase avec des underscores entre les mots.
    """
    # Supprime les caractères non alphanumériques (excepté les espaces et tirets)
    normalized_string = re.sub(r'[^\w\s-]', '', input_string, flags=re.UNICODE)

    # Remplace les espaces et tirets successifs par un espace unique
    normalized_string = re.sub(r'[\s-]+', ' ', normalized_string.strip())

    # Découpe la chaîne en mots et met la première lettre de chaque mot en majuscule
    words = normalized_string.split()
    snake_case_camel = '_'.join(word.capitalize() for word in words)

    # Ajoute un préfixe si la chaîne commence par un chiffre
    if re.match(r'^\d', snake_case_camel):
        snake_case_camel = f"Id_{snake_case_camel}"

    return snake_case_camel


def esc(input_string:str)->str:
    """
    Ajoute un backslash devant les caractères spéciaux dans une chaîne.

    @param input_string: La chaîne à traiter.
    @return: La chaîne avec les caractères spéciaux échappés.
    """
    # Définir les caractères spéciaux à échapper
    special_chars = r"`'\"*?\\"

    # Ajoute un backslash devant les caractères spéciaux
    escaped_string = re.sub(f"([{re.escape(special_chars)}])", r"\\\1", input_string)

    return escaped_string