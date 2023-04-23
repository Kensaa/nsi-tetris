"""Module contenant les tests du module tableaux"""

import unittest
from copy import deepcopy

from nsi_tetris.jeu.tableaux import tourner, parcourir


class TestTourner(unittest.TestCase):
    """Tests de la fonction tourner"""

    def test_effet_secondaire(self):
        """
        Vérifie que tourner ne modifie pas le tableau d'origine
        """
        tableau = [
            [1, 2],
            [4, 3],
        ]

        original = deepcopy(tableau)
        tourner(tableau)

        self.assertEqual(original, tableau)

    def test_horaire(self):
        """
        Vérifie que tourner fonctionne avec un argument valide dans le sens horaire
        """
        tableau1 = [
            [1, 2],
            [4, 3],
        ]
        tableau2 = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        tableau3 = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        self.assertEqual(
            tourner(tableau1),
            [
                [4, 1],
                [3, 2],
            ],
        )
        self.assertEqual(
            tourner(tableau2),
            [
                [7, 4, 1],
                [8, 5, 2],
                [9, 6, 3],
            ],
        )
        self.assertEqual(
            tourner(tableau3),
            [
                [13, 9, 5, 1],
                [14, 10, 6, 2],
                [15, 11, 7, 3],
                [16, 12, 8, 4],
            ],
        )

    def test_antihoraire(self):
        """
        Vérifie que tourner fonctionne avec un argument valide dans le sens antihoraire
        """
        tableau1 = [
            [1, 2],
            [4, 3],
        ]
        tableau2 = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        tableau3 = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        self.assertEqual(
            tourner(tableau1, False),
            [
                [2, 3],
                [1, 4],
            ],
        )
        self.assertEqual(
            tourner(tableau2, False),
            [
                [3, 6, 9],
                [2, 5, 8],
                [1, 4, 7],
            ],
        )
        self.assertEqual(
            tourner(tableau3, False),
            [
                [4, 8, 12, 16],
                [3, 7, 11, 15],
                [2, 6, 10, 14],
                [1, 5, 9, 13],
            ],
        )

    def test_erreurs(self):
        """
        Vérifie que tourner lève bien les bonnes erreurs
        """
        with self.assertRaises(TypeError):
            tourner("")  # type: ignore

        with self.assertRaises(TypeError):
            tourner([1, 5, 9])

    def test_4_rotations(self):
        """
        Vérifie qu'un tableau tourné quatre fois dans le même sens est identique à l'original
        """
        tableau = [
            [1, 2],
            [4, 3],
        ]

        # Sens horaire
        copie = deepcopy(tableau)
        for _ in range(4):
            copie = tourner(copie)

        self.assertEqual(tableau, copie)

        # Sens antihoraire
        copie = deepcopy(tableau)
        for _ in range(4):
            copie = tourner(copie, False)

        self.assertEqual(tableau, copie)


class TestParcourir(unittest.TestCase):
    """Test de la fonction parcourir"""

    def test_resultat(self):
        """
        Vérifie que la fonction parcourt bien le tableau dans le bon ordre, \
            et que les coordonnées des élements sont bonnes
        """
        tableau = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        self.assertEqual(
            list(parcourir(tableau)),
            [
                (1, 0, 0),
                (2, 0, 1),
                (3, 0, 2),
                (4, 1, 0),
                (5, 1, 1),
                (6, 1, 2),
                (7, 2, 0),
                (8, 2, 1),
                (9, 2, 2),
            ],
        )

    def test_erreurs(self):
        """Vérifie que parcourir renvoie bien les bonnes erreurs"""
        with self.assertRaises(TypeError):
            parcourir([1, 5, 9])  # type: ignore

        with self.assertRaises(TypeError):
            tourner(8)  # type: ignore


if __name__ == "__main__":
    unittest.main()
