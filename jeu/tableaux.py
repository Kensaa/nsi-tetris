"""Module contenant des fonctions relatives à la gestion de tableaux"""

from typing import TypeVar

T = TypeVar("T", tuple, list)


def tourner(tableau: T, sens=True) -> T:
    """
    Permet de tourner un tableau bidimensionnel (remplace la fonction rot90 de numpy)

    Args:
        tableau (T): Une liste ou un tuple à faire tourner
        sens (bool, optional): Le sens de rotation, où True correspond au sens des aiguilles
        d'une montre et False au sens inverse.

    Raises:
        TypeError: Le type du paramètre tableau est invalide

    Returns:
        T: Un tableau du même type correspondant au résultat de la rotation
    """
    if not isinstance(tableau, (list, tuple)):
        raise TypeError(
            f"Le paramètre tableau doit être de type list ou tuple, pas {type(tableau)}"
        )

    if sens:
        resultat = zip(*tableau[::-1])
    else:
        resultat = reversed(list(zip(*tableau)))

    if isinstance(tableau, tuple):
        return tuple(resultat)

    return list(resultat)
