"""Module du plateau de jeu"""

from typing import List, Tuple, Optional
from pygame.color import Color

from .erreurs import verif_entier_pos, verifier_type
from .constantes import GRILLE_LIGNES, GRILLE_COLONNES
from .tableaux import parcourir
from .tetrimino import Tetrimino

Case = Optional[Color]
Ligne = List[Case]
Grille = List[Ligne]


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

    def __deplacer(self, tetrimino: Tetrimino, colonnes: int) -> bool:
        """
        Décale horizontalement la position d'un tetrimino, mais uniquement si sa
        nouvelle position n'est pas obstruée ou invalide dans le contexte de la
        grille.
        La fonction renvoie True si la position du tetrimino a été modifiée, et
        False si le déplacement a échoué.

        Args:
            tetrimino (Tetrimino): Le tetrimino à déplacer
            colonnes (int): Le décalage appliqué à la coordonnée x du tetrimino

        Returns:
            bool: True si la position du tetrimino a été modifiée

        Raises:
            TypeError: Le type de tetrimino est invalide
            TypeError: Le type de colonnes est invalide
        """
        # Préconditions
        verifier_type("tetrimino", tetrimino, Tetrimino)
        verifier_type("colonnes", colonnes, int)

        x_initial = tetrimino.get_position()[0]
        tetrimino.set_position(x=x_initial + colonnes)
        if self.est_obstrue(tetrimino):
            tetrimino.set_position(x=x_initial)
            return False

        return True

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
        # Précondition
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
        # Précondition
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
            indice_ligne
            for indice_ligne in range(self.__lignes)
            if None not in self.__grille[indice_ligne]
        )

    def effacer_ligne(self, indice: int) -> None:
        """
        Efface une ligne de la grille et fait descendre toutes les lignes situées au dessus.

        Args:
            indice (int): L'indice de la ligne à effacer

        Raises:
            TypeError: Le type de la valeur passée à indice est invalide
            ValueError: L'indice se situe en dehors de la grille
        """
        # Préconditions
        verifier_type("indice", indice, int)
        if not 0 <= indice < self.__lignes:
            raise ValueError("indice doit correspondre à une ligne de la grille")

        # On efface la ligne
        ligne_vide: Ligne = [None] * self.__colonnes
        self.__grille[indice] = ligne_vide

        # On part de l'indice de la ligne effacée et on remonte jusqu'en haut de la
        # grille pour faire descendre les lignes du dessus
        for indice_sup in reversed(range(indice)):
            self.__grille[indice_sup + 1] = self.__grille[indice_sup]

    def deplacer_gauche(self, tetrimino: Tetrimino) -> bool:
        """
        Décale un tetrimino d'une case vers la gauche, mais uniquement si sa
        nouvelle position n'est pas obstruée ou invalide dans le contexte de la
        grille.
        La fonction renvoie True si la position du tetrimino a été modifiée, et
        False si le déplacement a échoué.

        Args:
            tetrimino (Tetrimino): Le tetrimino à déplacer

        Returns:
            bool: True si la position du tetrimino a été modifiée

        Raises:
            TypeError: Le type de tetrimino est invalide
        """
        # Précondition
        verifier_type("tetrimino", tetrimino, Tetrimino)

        return self.__deplacer(tetrimino, -1)

    def deplacer_droite(self, tetrimino: Tetrimino) -> bool:
        """
        Décale un tetrimino d'une case vers la droite, mais uniquement si sa
        nouvelle position n'est pas obstruée ou invalide dans le contexte de la
        grille.
        La fonction renvoie True si la position du tetrimino a été modifiée, et
        False si le déplacement a échoué.

        Args:
            tetrimino (Tetrimino): Le tetrimino à déplacer

        Returns:
            bool: True si la position du tetrimino a été modifiée

        Raises:
            TypeError: Le type de tetrimino est invalide
        """
        # Précondition
        verifier_type("tetrimino", tetrimino, Tetrimino)

        return self.__deplacer(tetrimino, 1)

    def tourner_tetrimino(self, tetrimino: Tetrimino, sens=True) -> bool:
        """
        Tourne un tetrimino, mais uniquement si sa nouvelle position n'est pas
        obstruée ou invalide dans le contexte de la grille.
        La fonction renvoie True si le tetrimino a été tourné, et False si la
        rotation a échoué.

        Args:
            tetrimino (Tetrimino): Le tetrimino à tourner
            sens (bool, optional): Le sens de rotation, où True correspond au sens des \
                aiguilles d'une montre et False au sens inverse.

        Returns:
            bool: True si la rotation du tetrimino a été modifiée

        Raises:
            TypeError: Le type de tetrimino est invalide
        """
        # Précondition
        verifier_type("tetrimino", tetrimino, Tetrimino)
        verifier_type("sens", sens, bool)

        tetrimino.tourner(sens)

        # Si la nouvelle position est invalide, on annule en tournant dans l'autre sens
        if self.est_obstrue(tetrimino):
            tetrimino.tourner(not sens)
            return False

        return True
