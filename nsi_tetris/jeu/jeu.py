"""Module du jeu"""

import sys
from typing import List

from pygame.time import Clock
from pygame.surface import Surface
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
    K_z,
    K_SPACE,
)
from pygame import (
    event as events,
    display,
    Rect,
    init as pygame_init,
    quit as pygame_quit,
)
from pygame.draw import rect
from pygame.color import Color
from nsi_tetris.jeu.sac import Sac
from nsi_tetris.jeu.plateau import Plateau
from nsi_tetris.jeu.tetrimino import Tetrimino
from nsi_tetris.jeu.erreurs import verifier_type
from nsi_tetris.jeu.constantes import (
    MODELES_TETRIMINOS,
    TETR_DEFAUT_X,
    TETR_DEFAUT_Y,
    TAILLE_FENETRE,
    IPS,
    TAILLE_CASE,
)
from nsi_tetris.jeu.tableaux import parcourir


class Jeu:
    """Représente l'état actuel du jeu"""

    def __init__(self) -> None:
        self.__plateau = Plateau()
        self.__sac = Sac(list(MODELES_TETRIMINOS.values()))
        self.__pause = False
        self.__nouveau_tetr()
        self.__chronometre = 0

    def __nouveau_tetr(self) -> None:
        # On crée le prochain tetrimino
        modele = self.__sac.depiler()
        tetr = Tetrimino(modele, TETR_DEFAUT_X, TETR_DEFAUT_Y)

        # On fait descendre le tetrimino d'une ligne si c'est possible
        tetr_y = tetr.get_position()[1]
        tetr.set_position(y=tetr_y + 1)
        if self.__plateau.est_obstrue(tetr):
            tetr.set_position(y=tetr_y)

        self.__tetr_actuel = tetr

    def afficher(self, surface: Surface, evenements: List[events.Event]) -> None:
        verifier_type("surface", surface, Surface)
        verifier_type("evenements", evenements, list)

        for evenement in evenements:
            if evenement.type == KEYDOWN:
                if evenement.key == K_ESCAPE:
                    self.__pause = not self.__pause

                if evenement.key == K_LEFT:
                    self.__plateau.deplacer_gauche(self.__tetr_actuel)

                if evenement.key == K_RIGHT:
                    self.__plateau.deplacer_droite(self.__tetr_actuel)

                if evenement.key == K_DOWN:
                    self.__chronometre = IPS

                if evenement.key == K_UP:
                    self.__plateau.tourner_tetrimino(self.__tetr_actuel, True)

                if evenement.key == K_z:
                    self.__plateau.tourner_tetrimino(self.__tetr_actuel, False)

                if evenement.key == K_SPACE:
                    fantome = self.__plateau.fantome(self.__tetr_actuel)
                    self.__tetr_actuel.set_position(y=fantome)
                    self.__chronometre = IPS

        # Lorsque le délai est écoulé, on fait descendre ou on verouille le tetrimino
        if self.__chronometre >= IPS:
            self.__chronometre = 0

            fantome = self.__plateau.fantome(self.__tetr_actuel)
            tetr_y = self.__tetr_actuel.get_position()[1]
            if tetr_y == fantome:
                self.__plateau.verrouiller(self.__tetr_actuel)
                self.__nouveau_tetr()
            else:
                self.__tetr_actuel.set_position(y=tetr_y + 1)

        # On affiche l'état du jeu sur la fenêtre
        lignes, colonnes = self.__plateau.forme()
        largeur_grille = colonnes * TAILLE_CASE
        hauteur_grille = lignes * TAILLE_CASE

        debut_x = (TAILLE_FENETRE[0] - largeur_grille) // 2
        debut_y = (TAILLE_FENETRE[1] - hauteur_grille) // 2

        # Affichage du plateau
        for element, ligne, colonne in parcourir(self.__plateau.grille()):
            couleur = element if element is not None else Color("white")
            rect_case = Rect(
                debut_x + colonne * TAILLE_CASE,
                debut_y + ligne * TAILLE_CASE,
                TAILLE_CASE,
                TAILLE_CASE,
            )

            rect(surface, couleur, rect_case)

        # Affichage du tetrimino en cours de chute
        couleur_tetr = self.__tetr_actuel.get_couleur()
        tetr_x, tetr_y = self.__tetr_actuel.get_position()
        for element, ligne, colonne in parcourir(self.__tetr_actuel.get_forme()):
            if element != 0:
                rect_case = Rect(
                    debut_x + (colonne + tetr_x) * TAILLE_CASE,
                    debut_y + (ligne + tetr_y) * TAILLE_CASE,
                    TAILLE_CASE,
                    TAILLE_CASE,
                )

                rect(surface, couleur_tetr, rect_case)
        
        # Affichage du fantome
        fantome_y = self.__plateau.fantome(self.__tetr_actuel)
        couleur_fantome = Color(couleur_tetr.r,couleur_tetr.g,couleur_tetr.b,100)
        for element, ligne, colonne in parcourir(self.__tetr_actuel.get_forme()):
            if element != 0:
                rect_case = Rect(
                    debut_x + (colonne + tetr_x) * TAILLE_CASE,
                    debut_y + (ligne + fantome_y) * TAILLE_CASE,
                    TAILLE_CASE,
                    TAILLE_CASE,
                )
                rect(surface, couleur_fantome, rect_case)
                
        # On incrémente le chronomètre
        self.__chronometre += 1


if __name__ == "__main__":
    # Initialisation
    pygame_init()
    fenetre = display.set_mode(TAILLE_FENETRE)
    horloge = Clock()
    jeu = Jeu()

    # Boucle du jeu
    while True:
        _evenements = events.get()
        for _evenement in _evenements:
            if _evenement.type == QUIT:
                pygame_quit()
                sys.exit(0)

        jeu.afficher(fenetre, _evenements)

        display.update()
        horloge.tick(IPS)
