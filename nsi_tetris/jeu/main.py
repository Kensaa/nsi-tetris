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
    from nsi_tetris.jeu.jeu import Jeu
    from nsi_tetris.jeu.constantes import TAILLE_FENETRE, IPS

    # Initialisation
    pygame_init()
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
