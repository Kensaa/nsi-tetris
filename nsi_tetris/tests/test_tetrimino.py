"""Module contenant les tests du module tetrimino"""

import unittest

from nsi_tetris.jeu.tetrimino import Tetrimino
from nsi_tetris.jeu.constantes import MODELES_TETRIMINOS


class TestConstructeur(unittest.TestCase):
    """Test du constructeur de la classe Tetrimino"""

    def test_erreurs(self):
        """
        Vérifie que le constructeur lève les bonnes erreurs
        """
        with self.assertRaises(TypeError):
            Tetrimino("")  # type: ignore

        with self.assertRaises(TypeError):
            Tetrimino((), "", 0)  # type: ignore

        with self.assertRaises(TypeError):
            Tetrimino((), 0, "")  # type: ignore

        with self.assertRaises(ValueError):
            Tetrimino(("", "", ""), 0, 0)  # type: ignore


class TestSetPosition(unittest.TestCase):
    """Test de la méthode set_position de la classe Tetrimino"""

    def test_erreurs(self):
        """Vérifie que la méthode lève bien les bonnes erreurs"""
        with self.assertRaises(TypeError):
            Tetrimino(MODELES_TETRIMINOS["I"]).set_position("", 0)  # type: ignore

        with self.assertRaises(TypeError):
            Tetrimino(MODELES_TETRIMINOS["I"]).set_position(0, "")  # type: ignore

    def test_fonctionnement(self):
        """Vérifie que la méthode fonctionne bien"""
        tetrimino = Tetrimino(MODELES_TETRIMINOS["I"], 0, 0)

        tetrimino.set_position(5, 7)
        self.assertEqual(tetrimino.get_position(), (5, 7))

        tetrimino.set_position(x=0)
        self.assertEqual(tetrimino.get_position(), (0, 7))

        tetrimino.set_position(y=9)
        self.assertEqual(tetrimino.get_position(), (0, 9))

        tetrimino.set_position()
        self.assertEqual(tetrimino.get_position(), (0, 9))


class TestRepr(unittest.TestCase):
    """Test de la représentation du tetrimino"""

    def test_resultat(self):
        """Vérifie que la méthode renvoie le bon résultat"""
        self.assertEqual(
            repr(Tetrimino(MODELES_TETRIMINOS["S"])),
            "Tetrimino(0, 0)\n⠀⠀████⠀⠀\n████",
        )

        self.assertEqual(
            repr(Tetrimino(MODELES_TETRIMINOS["I"])),
            "Tetrimino(0, 0)\n⠀⠀⠀⠀⠀⠀⠀⠀\n████████",
        )

        self.assertEqual(
            repr(Tetrimino(MODELES_TETRIMINOS["T"])),
            "Tetrimino(0, 0)\n⠀⠀██⠀⠀⠀⠀\n██████",
        )


if __name__ == "__main__":
    unittest.main()
