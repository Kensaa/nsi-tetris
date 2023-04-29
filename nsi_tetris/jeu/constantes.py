"""Module contenant les constantes"""

from typing import Dict
from pygame.color import Color

from .tetrimino import Modele

# Couleurs
BLANC = Color(255, 255, 255)
NOIR = Color(0, 0, 0)
TRANSPARENT = Color(0, 0, 0, 0)

# Affichage
TAILLE_FENETRE = (800, 600)
TAILLE_CASE = 18
TAILLE_BORDURE = 8
IPS = 60

# Position par défaut d'un tetrimino
TETR_DEFAUT_X = 3
TETR_DEFAUT_Y = 7

# Taille de la grille
GRILLE_LIGNES = 20
GRILLE_COLONNES = 10

# Le score que rapporte chaque nombre de lignes
SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

# Caractéristiques des différents tetriminos
MODELES_TETRIMINOS: Dict[str, Modele] = {
    "I": (
        (
            (0, 0, 0, 0),  #
            (1, 1, 1, 1),  #
            (0, 0, 0, 0),  #
            (0, 0, 0, 0),  #
        ),
        Color("cyan"),
    ),
    "O": (
        (
            (0, 0, 0, 0),  #
            (0, 1, 1, 0),  #
            (0, 1, 1, 0),  #
            (0, 0, 0, 0),  #
        ),
        Color("yellow"),
    ),
    "T": (
        (
            (0, 1, 0),  #
            (1, 1, 1),  #
            (0, 0, 0),  #
        ),
        Color("purple"),
    ),
    "S": (
        (
            (0, 1, 1),  #
            (1, 1, 0),  #
            (0, 0, 0),  #
        ),
        Color("green"),
    ),
    "Z": (
        (
            (1, 1, 0),  #
            (0, 1, 1),  #
            (0, 0, 0),  #
        ),
        Color("red"),
    ),
    "J": (
        (
            (1, 0, 0),  #
            (1, 1, 1),  #
            (0, 0, 0),  #
        ),
        Color("blue"),
    ),
    "L": (
        (
            (0, 0, 1),  #
            (1, 1, 1),  #
            (0, 0, 0),  #
        ),
        Color("orange"),
    ),
}
