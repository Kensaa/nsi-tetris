"""Module du jeu"""

import sys
from typing import List

from pygame.time import Clock
from pygame.color import Color
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
    SCORES,
    NOIR
)

from nsi_tetris.jeu.affichage import (
    afficher_plateau,
    afficher_tetrimino,
    afficher_texte
)

class Jeu:
    """Représente l'état actuel du jeu"""

    def __init__(self) -> None:
        self.__plateau = Plateau()
        self.__sac = Sac(list(MODELES_TETRIMINOS.values()))
        self.__pause = False
        self.__nouveau_tetr()
        self.__chronometre = 0
        self.__score = 0
        self.__perdu = False

    def __nouveau_tetr(self) -> None:
        # On crée le prochain tetrimino
        modele = self.__sac.depiler()
        tetr = Tetrimino(modele, TETR_DEFAUT_X, TETR_DEFAUT_Y)

        # On fait descendre le tetrimino d'une ligne si c'est possible
        if self.__plateau.est_obstrue(tetr):
            self.__perdu = True
        
        tetr_y = tetr.get_position()[1]
        tetr.set_position(y=tetr_y + 1)
        if self.__plateau.est_obstrue(tetr):
            tetr.set_position(y=tetr_y)

        self.__tetr_actuel = tetr

    def afficher(self, surface: Surface, evenements: List[events.Event]) -> None:
        verifier_type("surface", surface, Surface)
        verifier_type("evenements", evenements, list)

        # On efface le contenu de la fenêtre
        surface.fill(NOIR)

        for evenement in evenements:
            if evenement.type == KEYDOWN:
                if self.__perdu:
                    # on appelle le constructeur pour réinitialiser le jeu
                    self.__init__()
                else:
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
                # On verifie si des lignes sont completées
                lignes_completees = self.__plateau.lignes_completes()
                nombre_lignes = len(lignes_completees)
                if nombre_lignes > 0:
                    # des lignes sont complétées
                    self.__score += SCORES[nombre_lignes]
                    for index in lignes_completees:
                        self.__plateau.effacer_ligne(index)
                self.__nouveau_tetr()
            else:
                self.__tetr_actuel.set_position(y=tetr_y + 1)

        # Si le jeu est fini

        # On affiche l'état du jeu sur la fenêtre

        # On affiche le score
        texte = afficher_texte(f'Score: {self.__score}',24, None)
        surface.blit(texte, (0,0))

        lignes, colonnes = self.__plateau.forme()
        largeur_grille = colonnes * TAILLE_CASE
        hauteur_grille = lignes * TAILLE_CASE

        debut_x = (TAILLE_FENETRE[0] - largeur_grille) // 2
        debut_y = (TAILLE_FENETRE[1] - hauteur_grille) // 2

        # Affichage du plateau
        plateau = afficher_plateau(self.__plateau)
        surface.blit(plateau,(
            debut_x,
            debut_y
        ))

        # Affichage du tetrimino en cours de chute
        tetrimino = afficher_tetrimino(self.__tetr_actuel)
        tetr_x, tetr_y = self.__tetr_actuel.get_position()
        surface.blit(tetrimino,(
            debut_x + tetr_x * TAILLE_CASE,
            debut_y + tetr_y * TAILLE_CASE
            ))
        
        # Affichage du fantome du tetrimino
        fantome_x = tetr_x
        fantome_y = self.__plateau.fantome(self.__tetr_actuel)
        fantome = afficher_tetrimino(self.__tetr_actuel)
        fantome.set_alpha(100)
        surface.blit(fantome,(
            debut_x + fantome_x * TAILLE_CASE,
            debut_y + fantome_y * TAILLE_CASE
            ))
        
        if self.__perdu:
            texte_perdu = afficher_texte('PERDU',48, Color('black'))
            texte_recommencer = afficher_texte("appuyez sur n'importe quelle touche pour recommencer", 24, Color('black'))

            centre_x1, centre_y1 = texte_perdu.get_rect().center
            centre_x2, centre_y2 = texte_recommencer.get_rect().center

            surface.blit(texte_perdu,(
                TAILLE_FENETRE[0] // 2 - centre_x1,
                TAILLE_FENETRE[1] // 2- centre_y1
            ))
            surface.blit(texte_recommencer,(
                TAILLE_FENETRE[0] // 2- centre_x2,
                TAILLE_FENETRE[1] // 2- centre_y2 + 50
            ))
        else:
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
