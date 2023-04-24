"""Module contenant les tests du module tetrimino"""

import unittest

from nsi_tetris.jeu.tetrimino import Tetrimino
from nsi_tetris.jeu.constantes import MODELES_TETRIMINOS

class TestConstructeur(unittest.TestCase):
    """Test du constructeur de la classe Tetrimino"""

    def test_erreurs(self):
        """
        Vérifie que le constructeur lève les bonnes erreurs quand appelé avec les mauvais arguments
        s"""
        with self.assertRaises(TypeError):
            #1er arguement est un tuple
            Tetrimino('') # type: ignore

        with self.assertRaises(TypeError):
            #2eme arguement est un int
            Tetrimino((),'',0) # type: ignore

        with self.assertRaises(TypeError):
            #3eme arguement est un int
            Tetrimino((),0,'') # type: ignore
       
        with self.assertRaises(ValueError):
            #1eme arguement (tuple) contient deux élements
            Tetrimino(('','',''),0,0) # type: ignore

class TestSetPosition(unittest.TestCase):
    """Test de la méthode set_position de la classe Tetrimino"""

    def test_erreurs(self):
        """Vérifie que la méthode lève bien les bonnes erreurs"""
        with self.assertRaises(TypeError):
            #1er arguement est un int
            Tetrimino(MODELES_TETRIMINOS['I']).set_position('',0) #type: ignore
       
        with self.assertRaises(TypeError):
            #2eme arguement est un int
            Tetrimino(MODELES_TETRIMINOS['I']).set_position(0,'') #type: ignore

    def test_fonctionnement(self):
        """Vérifie que la méthode fonctionne bien"""
        tetrimino = Tetrimino(MODELES_TETRIMINOS['I'],0,0)
        tetrimino.set_position(5,7)
        self.assertEqual(tetrimino.get_position(),(5,7))


if __name__ == '__main__':
    unittest.main()
