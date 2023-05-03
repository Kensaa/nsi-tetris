"""Le module erreurs contient des fonctions permettant de tester les préconditions plus simplement."""

from typing import Type


def ou_erreur(condition: bool, type_erreur: Type[Exception], *args) -> None:
    """
    Lève une erreur si condition vaut False (équivaut à assert, mais permet de préciser
    le type et le contenu de l'erreur).

    Args:
        condition (bool): L'assertion à vérifier
        type_erreur (Type[Exception]): Le type de l'erreur
        Toute valeur supplémentaire sera passée au constructeur de l'erreur

    Raises:
        type_erreur: L'erreur levée si condition vaut False
    """
    if not condition:
        raise type_erreur(*args)


def verifier_type(nom: str, valeur, type_valide: Type) -> None:
    """
    Permet de vérifier le type d'une valeur passée en argument d'une fonction

    Args:
        nom (str): Le nom du paramètre
        valeur: La valeur passée
        type_valide (Type): Le type accepté par la fonction

    Raises:
        TypeError: La valeur ne correspond pas au type accepté par le paramètre de la fonction
    """
    ou_erreur(
        isinstance(valeur, type_valide),
        TypeError,
        f"Le paramètre {nom} doit être de type {type_valide.__name__}, pas {type(valeur).__name__}",
    )


def verif_entier_pos(nom: str, valeur: int) -> None:
    """Permet de vérifier qu'une valeur passée en argument d'une fonction est bien un entier positif

    Args:
        nom (str): Le nom du paramètre
        valeur (int): La valeur passée

    Raises:
        TypeError: La valeur n'est pas un entier
        ValueError: La valeur n'est pas positive
    """
    verifier_type(nom, valeur, int)
    ou_erreur(valeur >= 0, ValueError, f"{nom} doit être positif")
