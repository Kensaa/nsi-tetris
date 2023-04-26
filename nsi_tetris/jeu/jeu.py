"""Module du jeu"""

import sys
from typing import List

from pygame.time import Clock
from pygame.surface import Surface
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_z, K_SPACE
from pygame import event as events, display, init as pygame_init, quit as pygame_quit

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
    TAILLE_CASE
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
                if evenement.key == K_UP:
                    self.__plateau.tourner_tetrimino(self.__tetr_actuel, True)
                if evenement.key == K_z:
                    self.__plateau.tourner_tetrimino(self.__tetr_actuel, False)
                if evenement.key == K_SPACE:
                    nouvelle_hauteur = self.__plateau.fantome(self.__tetr_actuel)
                    self.__tetr_actuel.set_position(None, nouvelle_hauteur)
        
        if self.__chronometre >= IPS:
            self.__chronometre = 0

            fantome = self.__plateau.fantome(self.__tetr_actuel)
            position = self.__tetr_actuel.get_position()
            if position[1] == fantome:
                self.__plateau.verrouiller(self.__tetr_actuel)
                self.__nouveau_tetr()
            else:
                self.__tetr_actuel.set_position(None,position[1] + 1)

        # RENDER
        #longeur de la grille
        longueur_grille = self.__plateau.forme()[1] * TAILLE_CASE
        hauteur_grille = self.__plateau.forme()[0] * TAILLE_CASE
        #position en x du coin en haut a gauche de la grille
        debut_x = (TAILLE_FENETRE[0] - longueur_grille) // 2
        debut_y = TAILLE_FENETRE[1] - hauteur_grille

        for e, x, y in parcourir(self.__plateau.grille()):
            pass
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
