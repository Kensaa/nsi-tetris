"""Module contenant les tests du module plateau"""

import unittest
from pygame.color import Color


from nsi_tetris.jeu.plateau import Plateau, Grille
from nsi_tetris.jeu.constantes import MODELES_TETRIMINOS
from nsi_tetris.jeu.tetrimino import Tetrimino

C = Color("white")
N = None


def depuis_grille(grille: Grille) -> Plateau:
    """
    Permet de créer un plateau à partir d'un tableau existant, ce qui
    est normalement interdit

    Args:
        grille (Grille): Le tableau à utiliser

    Returns:
        Plateau: Le plateau correspondant à cette grille
    """
    lignes = len(grille)
    colonnes = len(grille[0])
    plateau = Plateau(lignes, colonnes)

    # pylint: disable=protected-access
    plateau._Plateau__lignes = lignes  # type: ignore
    plateau._Plateau__grille = grille  # type: ignore
    return plateau


class TestConstructeur(unittest.TestCase):
    """Tests du constructeur"""

    def test_erreurs(self):
        """Vérifie que le constructeur renvoie les bonnes erreurs"""
        with self.assertRaises(TypeError):
            Plateau("test", 8)  # type: ignore

        with self.assertRaises(TypeError):
            Plateau(10, [])  # type: ignore

        with self.assertRaises(ValueError):
            Plateau(5, -2)

        with self.assertRaises(ValueError):
            Plateau(-5, 0)


class TestForme(unittest.TestCase):
    """Tests de la méthode forme"""

    def test_resultat(self):
        """Vérifie que la méthode renvoie le bon résultat"""
        plat = Plateau(15, 26)
        self.assertEqual(plat.forme(),(25,26))

class TestGrille(unittest.TestCase):
    """Tests de la méthode grille"""

    def test_resultat(self):
        """Vérifie que la méthode renvoie le bon résultat"""
        plateau = depuis_grille(
            [
                [N, N, N],
                [N, N, C],
                [C, C, C],
            ]
        )

        self.assertEqual(
            plateau.grille(),
            (
                (N, N, N),
                (N, N, C),
                (C, C, C),
            ),
        )

class TestEstObstrue(unittest.TestCase):
    """Tests de la méthode est_obstrue"""

    def test_erreurs(self):
        """Vérifie que la méthode lève les bonnes erreurs"""
        with self.assertRaises(TypeError):
            Plateau(5,5).est_obstrue('') #type: ignore            

    def test_fonctionnement(self):
        """Vérifie que la méthode fonctionne bien"""
        plateau = Plateau(10,10)
        tetrimino1 = Tetrimino(MODELES_TETRIMINOS['J'])
        tetrimino1.set_position(9,0)
        self.assertTrue(plateau.est_obstrue(tetrimino1))
        
        tetrimino1.set_position(0,0)
        plateau.verrouiller(tetrimino1)
        tetrimino2 = Tetrimino(MODELES_TETRIMINOS['L'])
        self.assertTrue(plateau.est_obstrue(tetrimino2))

class TestVerrouiller(unittest.TestCase):
    """Tests de la méthode verouiller"""

    def test_erreurs(self):
        """Vérifie que la méthode lève les bonnes erreurs"""
        with self.assertRaises(TypeError):
            Plateau(5,5).verrouiller('') #type: ignore

    def test_fonctionnement(self):
        """Vérifie que la méthode fonctionne bien"""
        plateau = Plateau(10,10)
        tetrimino = Tetrimino(MODELES_TETRIMINOS['Z'])
        plateau.verrouiller(tetrimino)
        self.assertEqual(plateau.grille()[0][0],Color('red'))

class TestEffacerLigne(unittest.TestCase):
    """Tests de la méthode effacer_ligne"""
    def test_erreurs(self):
        """Vérifie que la méthode lève les bonnes erreurs"""
        with self.assertRaises(TypeError):
            Plateau(5,5).effacer_ligne('') #type: ignore
        
        with self.assertRaises(ValueError):
            Plateau(5,5).effacer_ligne(-1)
        
        with self.assertRaises(ValueError):
            Plateau(5,5).effacer_ligne(20)

    def test_fonctionnement(self):
        plateau = depuis_grille([
            [C,C,N,C],
            [N,C,C,N],
            [C,N,N,C],
            [C,C,C,C]
        ])
        plateau.effacer_ligne(2)
        self.assertEqual(plateau.grille(),(
            (N,N,N,N),
            (C,C,N,C),
            (N,C,C,N),
            (C,C,C,C)
        ))
if __name__ == "__main__":
    unittest.main()