"""Module du jeu"""

import sys
from pygame.time import Clock
from pygame.surface import Surface
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
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
)


class Jeu:
    """Représente l'état actuel du jeu"""

    def __init__(self) -> None:
        self.__plateau = Plateau()
        self.__sac = Sac(list(MODELES_TETRIMINOS.values()))
        self.__nouveau_tetr()

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

    def afficher(self, surface: Surface) -> None:
        verifier_type("surface", surface, Surface)


if __name__ == "__main__":
    # Initialisation
    pygame_init()
    fenetre = display.set_mode(TAILLE_FENETRE)
    horloge = Clock()

    # Boucle du jeu
    pause = False
    while True:
        evenements = events.get()
        for evenement in evenements:
            if evenement.type == QUIT:
                pygame_quit()
                sys.exit(0)

            if evenement.type == KEYDOWN and evenement.key == K_ESCAPE:
                pause = not pause

        display.update()
        horloge.tick(IPS)
