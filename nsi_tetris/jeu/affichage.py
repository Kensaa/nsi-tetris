"""Module d'affichage"""
from pygame.surface import Surface
from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from pygame.locals import SRCALPHA
from pygame.color import Color
from pygame.font import Font
import pygame

from typing import Optional
from nsi_tetris.jeu.tetrimino import Tetrimino
from nsi_tetris.jeu.plateau import Plateau
from nsi_tetris.jeu.constantes import (
    TAILLE_CASE,
    BLANC
)
from nsi_tetris.jeu.tableaux import parcourir


def afficher_plateau(plateau: Plateau) -> Surface:
    """Renvoie une surface contenant le plateau,
       avec des cases blanches lorque les cases sont vides
       ou la couleur de la case sinon  

    Args:
        plateau (Plateau): le plateau à dessiner

    Returns:
        Surface: la surface contenant le plateau
    """
    longeur = plateau.forme()[1] * TAILLE_CASE
    hauteur = plateau.forme()[0] * TAILLE_CASE
    surface = Surface((longeur, hauteur),SRCALPHA)

    for element, ligne, colonne in parcourir(plateau.grille()):
            couleur = element if element is not None else Color("white")
            rect_case = Rect(
                colonne * TAILLE_CASE,
                ligne * TAILLE_CASE,
                TAILLE_CASE,
                TAILLE_CASE,
            )

            draw_rect(surface, couleur, rect_case)
    return surface

def afficher_tetrimino(tetrimino: Tetrimino) -> Surface:
    """Renvoie une surface contenant le tetrimino

    Args:
        tetrimino (Tetrimino): la tetrimino à dessiner

    Returns:
        Surface: la surface contenant le tetrimino
    """
    longeur = len(tetrimino.get_forme()[0]) * TAILLE_CASE
    hauteur = len(tetrimino.get_forme()) * TAILLE_CASE
    surface = Surface((longeur, hauteur),SRCALPHA)
    
    couleur_tetr = tetrimino.get_couleur()
    for element, ligne, colonne in parcourir(tetrimino.get_forme()):
        if element != 0:
            rect_case = Rect(
                colonne * TAILLE_CASE,
                ligne * TAILLE_CASE,
                TAILLE_CASE,
                TAILLE_CASE,
            )

            draw_rect(surface, couleur_tetr, rect_case)
    return surface
    
def afficher_texte(texte: str, taille: int, arriere: Optional[Color]) -> Surface:
    """Renvoie une surface contenant le texte

    Args:
        texte (str): le texte à écrire

    Returns:
        Surface: la surface contenant le texte
    """
    police = Font(pygame.font.get_default_font(), taille)
    return police.render(texte, True, BLANC, arriere)
