"""Module du sac dans lequel on pioche aléatoirement les tetriminos"""

from typing import List
from random import shuffle

from .erreurs import verifier_type
from .tetrimino import Modele


class Sac:
    """Représente le générateur aléatoire de tetriminos"""

    def __init__(self, modeles: List[Modele]) -> None:
        verifier_type("modeles", modeles, list)
        if len(modeles) < 1:
            raise ValueError("Le sac doit contenir au moins 1 type de tetrimino")

        self.__modeles = modeles
        self.__contenu: List[Modele] = []

    def remplir(self, quantite: int) -> None:
        """
        Ajoute des modèles dans le sac jusqu'à ce qu'il contienne un certain nombre
        de modèles.

        Args:
            quantite (int): Le nombre de modèles, un entier supérieur ou égal à 1

        Raises:
            TypeError: Le type de quantite est invalide
            ValueError: La valeur de quantite est inférieure à 1
        """
        verifier_type("quantite", quantite, int)
        if quantite < 1:
            raise ValueError("La quantité doit être supérieure ou égale à 1")

        # Tant qu'il n'y a pas assez de modèles dans le sac,
        # on mélange les modèles et on les ajoute au sac
        while len(self.__contenu) < quantite:
            suite = self.__modeles.copy()
            shuffle(suite)
            self.__contenu += suite

    def depiler(self) -> Modele:
        """Renvoie le modèle du prochain tetrimino

        Returns:
            Modele: Un modèle de tetrimino
        """
        self.remplir(1)
        return self.__contenu.pop(0)
