"""
Le module jeu contient la partie "logique" du jeu avec
les étapes qui sont executées à chaque étape et l'affichage à l'écran.
"""

from typing import List

from pygame.rect import Rect
from pygame.surface import Surface
from pygame import draw, event as events
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
    K_z,
    K_SPACE,
)

from nsi_tetris.jeu.sac import Sac
from nsi_tetris.jeu.plateau import Plateau
from nsi_tetris.jeu.tetrimino import Tetrimino
from nsi_tetris.jeu.erreurs import verifier_type
from nsi_tetris.jeu.constantes import (
    BLANC,
    MODELES_TETRIMINOS,
    TAILLE_BORDURE,
    TETR_DEFAUT_X,
    TETR_DEFAUT_Y,
    IPS,
    TAILLE_CASE,
    SCORES,
    NOIR,
)
from nsi_tetris.jeu.affichage import (
    afficher_plateau,
    afficher_tetrimino,
    afficher_texte,
    centrer,
)


class Jeu:
    """Représente l'état actuel du jeu"""

    def __init__(self) -> None:
        self.__plateau = Plateau()
        self.__sac = Sac(list(MODELES_TETRIMINOS.values()))
        self.__score = 0
        self.__chronometre = 0
        self.__pause = False
        self.__perdu = False
        self.__nouveau_tetr()

    def __nouveau_tetr(self) -> None:
        # On crée le prochain tetrimino
        modele = self.__sac.depiler()
        tetr = Tetrimino(modele, TETR_DEFAUT_X, TETR_DEFAUT_Y)

        # Si la position initiale du tetrimino est obstruée, le joueur a perdu
        if self.__plateau.est_obstrue(tetr):
            self.__perdu = True
        else:
            # On fait descendre le tetrimino d'une ligne si c'est possible,
            # conformément au système de génération de Tetris
            tetr_y = tetr.get_position()[1]
            tetr.set_position(y=tetr_y + 1)
            if self.__plateau.est_obstrue(tetr):
                tetr.set_position(y=tetr_y)

            self.__tetr_actuel = tetr

    def avancer(self, evenements: List[events.Event]) -> None:
        """
        Fait avancer l'état du jeu d'une image en gérant les évènements

        Args:
            evenements (List[events.Event]): Les évènements pygame à utiliser

        Raises:
            TypeError: Le type de evenements est invalide
        """
        # Précondition
        verifier_type("evenements", evenements, list)

        # Gestion des évènements
        for evenement in evenements:
            if evenement.type == KEYDOWN:
                if self.__perdu:
                    # On réinitialise l'état du jeu
                    self.__init__()  # pylint: disable=unnecessary-dunder-call
                else:
                    if evenement.key == K_ESCAPE:
                        self.__pause = not self.__pause

                    if not self.__pause:
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

        # On incrémente le chronomètre
        if not (self.__perdu or self.__pause):
            self.__chronometre += 1

        # Lorsque le délai est écoulé, on actualise le tetrimino
        if self.__chronometre >= IPS:
            self.__chronometre = 0

            tetr_y = self.__tetr_actuel.get_position()[1]
            fantome = self.__plateau.fantome(self.__tetr_actuel)

            if tetr_y == fantome:
                # Le tetrimino touche le sol, on le verrouille
                self.__plateau.verrouiller(self.__tetr_actuel)

                # On verifie si des lignes sont completées
                lignes_completees = self.__plateau.lignes_completes()
                nombre_lignes = len(lignes_completees)
                if nombre_lignes > 0:
                    self.__score += SCORES[nombre_lignes]
                    for indice in lignes_completees:
                        self.__plateau.effacer_ligne(indice)

                self.__nouveau_tetr()
            else:
                # Le tetrimino peut continuer, on le fait descendre
                self.__tetr_actuel.set_position(y=tetr_y + 1)

    def afficher(self, surface: Surface) -> None:
        """Affiche l'état actuel du jeu sur une surface

        Args:
            surface (Surface): La surface à utiliser

        Raises:
            TypeError: Le type de surface est invalide
        """
        # Précondition
        verifier_type("surface", surface, Surface)

        # On efface le contenu de la fenêtre
        surface.fill(NOIR)

        # On récupère la taille et les coordonnées de la grille
        lignes, colonnes = self.__plateau.get_taille()
        largeur_grille = colonnes * TAILLE_CASE
        hauteur_grille = lignes * TAILLE_CASE

        grille_x = (surface.get_width() - largeur_grille) // 2
        grille_y = (surface.get_height() - hauteur_grille) // 2

        # Affichage du plateau
        rect_bordure = Rect(
            grille_x - TAILLE_BORDURE,
            grille_y - TAILLE_BORDURE,
            largeur_grille + TAILLE_BORDURE * 2,
            hauteur_grille + TAILLE_BORDURE * 2,
        )
        draw.rect(surface, BLANC, rect_bordure, TAILLE_BORDURE, TAILLE_BORDURE)
        plateau = afficher_plateau(self.__plateau)
        surface.blit(plateau, (grille_x, grille_y))

        # Affichage du tetrimino en cours de chute
        tetr_surf = afficher_tetrimino(self.__tetr_actuel)
        tetr_x, tetr_y = self.__tetr_actuel.get_position()
        surface.blit(
            tetr_surf,
            (grille_x + tetr_x * TAILLE_CASE, grille_y + tetr_y * TAILLE_CASE),
        )

        # Affichage du fantome du tetrimino
        fantome_y = self.__plateau.fantome(self.__tetr_actuel)
        fantome_surf = afficher_tetrimino(self.__tetr_actuel)
        fantome_surf.set_alpha(100)
        surface.blit(
            fantome_surf,
            (grille_x + tetr_x * TAILLE_CASE, grille_y + fantome_y * TAILLE_CASE),
        )

        # On affiche le score
        texte_score = afficher_texte(f"Score: {self.__score}", 24)
        surface.blit(
            texte_score,
            (
                surface.get_rect().centerx - texte_score.get_rect().centerx,
                grille_y + TAILLE_BORDURE,
            ),
        )

        # Affichage du texte pause
        if self.__pause:
            texte_pause = afficher_texte("PAUSE", 48, NOIR)
            surface.blit(texte_pause, centrer(surface, texte_pause))

        # Affichage de l'écran de fin
        if self.__perdu:
            texte_perdu = afficher_texte("PERDU", 48, NOIR)
            texte_recommencer = afficher_texte(
                "Appuyez sur n'importe quelle touche pour recommencer",
                24,
                NOIR,
            )

            rect_recommencer = texte_recommencer.get_rect()
            rect_recommencer.update(
                centrer(surface, texte_recommencer), rect_recommencer.size
            )

            surface.blit(
                texte_perdu,
                centrer(surface, texte_perdu),
            )
            surface.blit(
                texte_recommencer,
                rect_recommencer.move(0, 32).topleft,
            )
