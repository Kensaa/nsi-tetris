"""
Le module affichage contient des fonctions permettant d'obtenir des surfaces
à partir de structures de données comme les tetriminos pour les dessiner à l'écran
"""

from typing import Optional, Tuple

from pygame.surface import Surface
from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from pygame.locals import SRCALPHA
from pygame.color import Color
from pygame.font import Font, get_default_font

from nsi_tetris.jeu.erreurs import verifier_type
from nsi_tetris.jeu.tetrimino import Tetrimino
from nsi_tetris.jeu.plateau import Plateau
from nsi_tetris.jeu.constantes import TAILLE_CASE, BLANC
from nsi_tetris.jeu.tableaux import parcourir


def afficher_plateau(plateau: Plateau) -> Surface:
    """
    Dessine un plateau et renvoie la surface

    Args:
        plateau (Plateau): Le plateau à dessiner

    Raises:
        TypeError: Le type de plateau est invalide

    Returns:
        Surface: La surface contenant le plateau
    """
    # Précondition
    verifier_type("plateau", plateau, Plateau)

    lignes, colonnes = plateau.get_taille()
    largeur = colonnes * TAILLE_CASE
    hauteur = lignes * TAILLE_CASE
    surface = Surface((largeur, hauteur), SRCALPHA)

    for couleur_case, ligne, colonne in parcourir(plateau.get_grille()):
        if couleur_case is not None:
            rect_case = Rect(
                colonne * TAILLE_CASE,
                ligne * TAILLE_CASE,
                TAILLE_CASE,
                TAILLE_CASE,
            )

            draw_rect(surface, couleur_case, rect_case)

    return surface


def afficher_tetrimino(tetrimino: Tetrimino) -> Surface:
    """
    Dessine un tetrimino et renvoie la surface

    Args:
        tetrimino (Tetrimino): Le tetrimino à dessiner

    Raises:
        TypeError: Le type de tetrimino est invalide

    Returns:
        Surface: La surface contenant le tetrimino
    """
    # Précondition
    verifier_type("tetrimino", tetrimino, Tetrimino)

    largeur = len(tetrimino.get_forme()[0]) * TAILLE_CASE
    hauteur = len(tetrimino.get_forme()) * TAILLE_CASE
    surface = Surface((largeur, hauteur), SRCALPHA)

    couleur_tetr = tetrimino.get_couleur()
    for bit, ligne, colonne in parcourir(tetrimino.get_forme()):
        if bit != 0:
            rect_case = Rect(
                colonne * TAILLE_CASE,
                ligne * TAILLE_CASE,
                TAILLE_CASE,
                TAILLE_CASE,
            )

            draw_rect(surface, couleur_tetr, rect_case)

    return surface


def afficher_texte(texte: str, taille: int, arriere: Optional[Color] = None) -> Surface:
    """
    Dessine du texte et renvoie la surface

    Args:
        texte (str): Le texte à dessiner
        taille (int): La taille du texte
        arriere (Color, optional): La couleur d'arrière plan

    Raises:
        TypeError: Le type de texte est invalide
        TypeError: Le type de taille est invalide
        TypeError: Le type de arriere est invalide
        ValueError: La taille du texte doit être positive

    Returns:
        Surface: La surface contenant le texte
    """
    # Préconditions
    verifier_type("texte", texte, str)
    verifier_type("taille", taille, int)

    if arriere is not None:
        verifier_type("arriere", arriere, Color)

    if taille < 0:
        raise ValueError("La taille du texte doit être supérieure à 0")

    police = Font(get_default_font(), taille)
    return police.render(texte, True, BLANC, arriere)


def centrer(surface_a: Surface, surface_b: Surface) -> Tuple[int, int]:
    """
    Renvoie les coordonnées permettant de centrer une surface b dans une surface a

    Args:
        surface_a (Surface): La surface contenant l'autre surface
        surface_b (Surface): La surface à centrer

    Raises:
        TypeError: Le type de surface_a est invalide
        TypeError: Le type de surface_b est invalide

    Returns:
        Tuple[int, int]: Les coordonnées permettant de centrer la surface b dans la surface a
    """
    # Préconditions
    verifier_type("a", surface_a, Surface)
    verifier_type("b", surface_b, Surface)

    a_centrex, a_centrey = surface_a.get_rect().center
    b_centrex, b_centrey = surface_b.get_rect().center

    return (a_centrex - b_centrex, a_centrey - b_centrey)
