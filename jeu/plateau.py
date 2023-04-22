"""Module du plateau de jeu"""

from typing import List, Tuple, Optional
from pygame.color import Color

from erreurs import verif_entier_pos, verifier_type
from constantes import GRILLE_LIGNES, GRILLE_COLONNES
from tableaux import parcourir
from tetrimino import Tetrimino

Case = Optional[Color]
Grille = List[List[Case]]


class Plateau:
    """
    Représente le plateau de jeu.

    La grille mesure en réalité 10 lignes de plus afin de pouvoir gérer les tetriminos
    placés hors de la zone de jeu en fin de partie.
    """

    def __init__(
        self,
        lignes=GRILLE_LIGNES,
        colonnes=GRILLE_COLONNES,
    ) -> None:
        verif_entier_pos("lignes", lignes)
        verif_entier_pos("colonnes", colonnes)

        # On crée la grille, en utilisant la valeur None pour les cases vides
        self.__colonnes = colonnes
        self.__lignes = lignes + 10
        self.__grille: Grille = [[None] * self.__colonnes] * self.__lignes

    def __hors_limites(self, x: int, y: int) -> bool:
        """
        Renvoie True si les coordonnées (x;y) se situent hors de la grille.
        Si cette fonction renvoie False, alors self.__grille[y][x] existe.

        Args:
            x (int): La coordonnée en x
            y (int): La coordonnée en y

        Returns:
            bool: True si les coordonnées sont en dehors de la grille
        """
        x_invalide = x < 0 or x >= self.__colonnes
        y_invalide = y < 0 or y >= self.__lignes
        return x_invalide or y_invalide

    def forme(self) -> Tuple[int, int]:
        """
        Renvoie la forme de la grille dans un tuple au format (lignes, colonnes).
        Le nombre de lignes inclut les 10 lignes supplémentaires en haut de la grille.

        Returns:
            Tuple[int, int]: La forme de la grille au format (lignes, colonnes)
        """
        return self.__lignes, self.__colonnes

    def grille(self) -> Tuple[Tuple[Case]]:
        """
        Renvoie l'état actuel de la grille sous la forme d'un tuple de tuples.

        Returns:
            Tuple[Tuple[Case]]: Une copie immutable de la grille
        """
        lignes = (map(tuple, ligne) for ligne in self.__grille)  # type: ignore
        return tuple(*lignes)

    def est_obstrue(self, tetrimino: Tetrimino) -> bool:
        """
        Renvoie True si un tetrimino est hors de la grille ou dans une position obstruée.

        Args:
            tetrimino (Tetrimino): Le tetrimino à vérifier

        Returns:
            bool: True si la position du tetrimino est obstruée ou hors de la grille

        Raises:
            TypeError: La valeur passée en argument n'est pas un tetrimino
        """
        verifier_type("tetrimino", tetrimino, Tetrimino)

        tetr_x, tetr_y = tetrimino.get_position()
        for case, ligne, colonne in parcourir(tetrimino.get_forme()):
            if case != 0:
                case_x = colonne + tetr_x
                case_y = ligne + tetr_y
                if (
                    self.__hors_limites(case_x, case_y)
                    or self.__grille[case_y][case_x] is not None
                ):
                    return True

        return False

    def verrouiller(self, tetrimino: Tetrimino) -> None:
        """Ajoute un tetrimino au contenu de la grille

        Args:
            tetrimino (Tetrimino): Le tetrimino à poser dans la grille

        Raises:
            TypeError: La valeur passée en argument n'est pas un tetrimino
        """
        verifier_type("tetrimino", tetrimino, Tetrimino)

        tetr_x, tetr_y = tetrimino.get_position()
        couleur = tetrimino.get_couleur()
        for case, ligne, colonne in parcourir(tetrimino.get_forme()):
            if case != 0:
                case_x = colonne + tetr_x
                case_y = ligne + tetr_y
                self.__grille[case_y][case_x] = couleur

    def lignes_completes(self) -> Tuple[int, ...]:
        """
        Renvoie un tuple contenant les indices des lignes remplies de la grille s'il y en a.

        Returns:
            Tuple[int, ...]: Un tuple d'indices correspondant aux lignes pleines
        """
        return tuple(
            index_ligne
            for index_ligne in range(self.__lignes)
            if None not in self.__grille[index_ligne]
        )
