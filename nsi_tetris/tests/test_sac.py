"""Module contenant les tests du module tableaux"""

import unittest

from nsi_tetris.jeu.sac import Sac
from nsi_tetris.jeu.constantes import MODELES_TETRIMINOS


class TestConstructeur(unittest.TestCase):
    """Tests du constructeur"""

    def test_erreurs(self):
        """Vérifie que le constructeur renvoie les bonnes erreurs"""
        with self.assertRaises(TypeError):
            Sac("test")  # type: ignore

        with self.assertRaises(ValueError):
            Sac([])


class TestRemplir(unittest.TestCase):
    """Tests de la méthode remplir"""

    def test_erreurs(self):
        """Vérifie que remplir renvoie les bonnes erreurs"""

        sac = Sac(list(MODELES_TETRIMINOS.values()))

        with self.assertRaises(TypeError):
            sac.remplir("test")  # type: ignore

        with self.assertRaises(ValueError):
            sac.remplir(0)

        with self.assertRaises(ValueError):
            sac.remplir(-1)


if __name__ == "__main__":
    unittest.main()
