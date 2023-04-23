"""Module contenant les tests du module tableaux"""

import unittest
from copy import deepcopy

from nsi_tetris.jeu.tableaux import tourner


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
        tableau = [
            [1, 2],
            [4, 3],
        ]

        self.assertEqual(
            tourner(tableau),
            [
                [4, 1],
                [3, 2],
            ],
        )


if __name__ == "__main__":
    unittest.main()
