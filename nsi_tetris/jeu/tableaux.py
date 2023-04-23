"""Module contenant des fonctions relatives à la gestion de tableaux"""

from typing import Generator, Tuple, TypeVar, Iterable

T = TypeVar("T", tuple, list)
E = TypeVar("E")


def tourner(tableau: T, sens=True) -> T:
    """
    Permet de tourner un tableau bidimensionnel (remplace la fonction rot90 de numpy).
    Une très bonne explication du code utilisé peut être trouvée à cette adresse:
    https://stackoverflow.com/a/8421412

    Args:
        tableau (T): Une liste ou un tuple à faire tourner
        sens (bool, optional): Le sens de rotation, où True correspond au sens des aiguilles
        d'une montre et False au sens inverse.

    Raises:
        TypeError: Le type du paramètre tableau est invalide

    Returns:
        T: Un tableau du même type correspondant au résultat de la rotation
    """

    # Précondition
    if not isinstance(tableau, (list, tuple)):
        raise TypeError(
            f"Le paramètre tableau doit être de type list ou tuple, pas {type(tableau)}"
        )

    try:
        # Rotation du tableau
        if sens:
            resultat = map(list, zip(*tableau[::-1]))
        else:
            lignes = map(list, zip(*tableau))
            resultat = reversed(list(lignes))
    except TypeError as erreur:
        # zip() lève une erreur si les éléments ne sont pas itérables,
        # donc on attrape l'erreur pour l'expliquer plus clairement
        message = str(erreur)
        if message.endswith("object is not iterable"):
            raise TypeError("Le paramètre tableau doit être bidimensionnel") from erreur

        # Si l'erreur a une autre raison inattendue on la lève à nouveau
        # sans modifier le message
        raise erreur

    # On renvoie le résultat en respectant le type d'origine
    if isinstance(tableau, tuple):
        return tuple(resultat)

    return list(resultat)


def parcourir(
    iterable: Iterable[Iterable[E]],
) -> Generator[Tuple[E, int, int], None, None]:
    """
    Permet d'itérer sur tous les élements (de type E) d'une structure itérable à deux dimensions

    Args:
        tableau (Iterable[Iterable[E]]): Un itérable à deux dimensions

    Raises:
        TypeError: Le paramètre tableau doit être un itérable bidimensionnel

    Yields:
        Tuple[E, int, int]: Un tuple content l'élément et ses coordonnées
    """
    try:
        for index_ligne, ligne in enumerate(iterable):
            for index_colonne, element in enumerate(ligne):
                yield element, index_ligne, index_colonne
    except TypeError as erreur:
        # Même fonctionnement que dans la fonction tourner
        message = str(erreur)
        if message.endswith("object is not iterable"):
            raise TypeError(
                "Le paramètre tableau doit être un itérable bidimensionnel"
            ) from erreur

        raise erreur
