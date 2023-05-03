"""Le module tetrimino contient une classe qui représente un tetrimino du jeu"""

from typing import Optional, Tuple, Literal
from pygame.color import Color

from .erreurs import verifier_type
from .tableaux import tourner

# Définition des types permettant de caractériser un tetrimino
# La forme d'un tetrimino est représenter par un tuple à deux dimensions
# où chaque case contient 0 ou 1
Bit = Literal[0, 1]
Ligne = Tuple[Bit, ...]
Forme = Tuple[Ligne, ...]
Modele = Tuple[Forme, Color]


class Tetrimino:
    """
    Représente un tetrimino.

    Un tetrimino est caractérisé par une forme, une couleur et une position.
    Les attributs de position ne sont pas utilisés par les méthodes de cette classe et servent
    uniquement à contenir des informations relatives à un autre contexte comme une grille ou une
    fenêtre par exemple.
    """

    def __init__(
        self,
        modele: Modele,
        x=0,
        y=0,
    ) -> None:
        # Préconditions
        verifier_type("modele", modele, tuple)
        verifier_type("x", x, int)
        verifier_type("y", y, int)

        if len(modele) != 2:
            raise ValueError(
                f"Le modèle du tetrimino doit contenir deux éléments, pas {len(modele)}"
            )

        # Création des attributs
        self.__forme, self.__couleur = modele
        self.__x = x
        self.__y = y

    def __repr__(self) -> str:
        # On commence par le nom de la classe et la position du tetrimino
        resultat = f"Tetrimino({self.__x}, {self.__y})\n"

        # On ajoute la forme
        for ligne in self.__forme:
            for bit in ligne:
                # On choisit le caractère approprié et on le multiplie par deux
                # pour compenser le fait que les caractères sont plus grands en hauteur
                resultat += ("\u2800" if bit == 0 else "\u2588") * 2

            resultat += "\n"

        # On renvoie le résultat en enlevant les caractères vides en fin de chaîne
        return resultat.rstrip("\u2800\n")

    def get_forme(self) -> Forme:
        """Renvoie la forme du tetrimino"""
        return self.__forme

    def get_couleur(self) -> Color:
        """Renvoie la couleur du tetrimino"""
        return self.__couleur

    def get_position(self) -> Tuple[int, int]:
        """Renvoie la position du tetrimino"""
        return self.__x, self.__y

    def set_position(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> None:
        """
        Modifie la position du tetrimino.
        Si un paramètre est laissé vide, la coordonnée correspondante n'est pas modifiée.

        Args:
            x (int, optional): La nouvelle coordonnée en x. Vide par défaut.
            y (int, optional): La nouvelle coordonnée en y. Vide par défaut.

        Raises:
            TypeError: Le type de x est invalide
            TypeError: Le type de y est invalide
        """
        if x is not None:
            verifier_type("x", x, int)
            self.__x = x

        if y is not None:
            verifier_type("y", y, int)
            self.__y = y

    def tourner(self, sens_horaire=True) -> None:
        """
        Applique une rotation de 90° au tetrimino

        Args:
            sens_horaire (bool, optional): Le sens de rotation, où True correspond au sens \
                des aiguilles d'une montre et False au sens inverse.
        """
        self.__forme = tourner(self.__forme, sens_horaire)
