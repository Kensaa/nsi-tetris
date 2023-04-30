"""Fichier exécutable du jeu"""

import sys

from pygame.locals import QUIT
from pygame.time import Clock
from pygame import (
    event as events,
    display,
    init as pygame_init,
    quit as pygame_quit,
)


if __name__ == "__main__":
    # Ajout à la variable PYTHONPATH le temps de l'exécution pour pouvoir importer le reste du jeu
    sys.path.append("..")

    from nsi_tetris.jeu.jeu import Jeu
    from nsi_tetris.jeu.affichage import afficher_tetrimino
    from nsi_tetris.jeu.tetrimino import Tetrimino
    from nsi_tetris.jeu.constantes import MODELES_TETRIMINOS
    from nsi_tetris.jeu.constantes import TAILLE_FENETRE, IPS

    # Initialisation
    pygame_init()
    tetr_icon = Tetrimino(MODELES_TETRIMINOS["S"])
    display.set_caption("nsi-tetris")
    display.set_icon(afficher_tetrimino(tetr_icon))
    fenetre = display.set_mode(TAILLE_FENETRE)
    horloge = Clock()
    jeu = Jeu()

    # Boucle du jeu
    while True:
        evenements = events.get()
        for evenement in evenements:
            if evenement.type == QUIT:
                pygame_quit()
                sys.exit(0)

        jeu.avancer(evenements)
        jeu.afficher(fenetre)

        display.update()
        horloge.tick(IPS)
