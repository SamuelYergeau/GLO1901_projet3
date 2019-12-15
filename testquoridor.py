"""Module pour tester quoridor.py
"""
import unittest
import networkx as nx
from quoridor import Quoridor
from quoridor import QuoridorError


class TestQuoridor(unittest.TestCase):
    """classe test quoridor"""
    def test__init__(self):
        """test la fonction __init
            Cas à tester:
                - Création d'une partie nouvelle
                - Création d'une partie existante
                - QuoridorError si 'joueur' n'est pas de longueur 2
                - QuoridorError si le nombre de murs plaçable est 0 > n >10
                - QuoridorError si la position d'un joueur est invalide
                - QuoridorError si l'argument 'mur' n'est pas un dictionnaire si présent
                - QuoridorError si le total des murs placés et plaçables n'est pas 20
                - QuoridorError si la position d'un mur est invalide
        """
        # Dresser des rootaux connus pour des constructions connues
        nouveau_jeu = ("légende: 1=foo 2=bar\n" +
                       "   -----------------------------------\n" +
                       "9 | .   .   .   .   2   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "8 | .   .   .   .   .   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "7 | .   .   .   .   .   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "6 | .   .   .   .   .   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "5 | .   .   .   .   .   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "4 | .   .   .   .   .   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "3 | .   .   .   .   .   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "2 | .   .   .   .   .   .   .   .   . |\n" +
                       "  |                                   |\n" +
                       "1 | .   .   .   .   1   .   .   .   . |\n" +
                       "--|-----------------------------------\n" +
                       "  | 1   2   3   4   5   6   7   8   9\n")
        partie_existante_rootau = ("légende: 1=foo 2=bar\n" +
                                   "   -----------------------------------\n" +
                                   "9 | .   .   .   .   .   .   .   .   . |\n" +
                                   "  |                                   |\n" +
                                   "8 | .   .   .   .   .   . | .   .   . |\n" +
                                   "  |        ------- -------|-------    |\n" +
                                   "7 | .   .   .   .   2   . | .   .   . |\n" +
                                   "  |                                   |\n" +
                                   "6 | . | .   .   .   1   . | .   .   . |\n" +
                                   "  |   |-------            |           |\n" +
                                   "5 | . | .   . | .   .   . | .   .   . |\n" +
                                   "  |           |                       |\n" +
                                   "4 | .   .   . | .   .   .   .   .   . |\n" +
                                   "  |            -------                |\n" +
                                   "3 | .   .   .   .   . | .   .   .   . |\n" +
                                   "  |                   |               |\n" +
                                   "2 | .   .   .   .   . | .   .   .   . |\n" +
                                   "  |                                   |\n" +
                                   "1 | .   .   .   .   .   .   .   .   . |\n" +
                                   "--|-----------------------------------\n" +
                                   "  | 1   2   3   4   5   6   7   8   9\n")
        partie_existante_etat = {
            "joueurs": [
                {"nom": "foo", "murs": 7, "pos": [5, 6]},
                {"nom": "bar", "murs": 3, "pos": [5, 7]}
            ],
            "murs": {
                "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
            }}
        # Test de création d'une partie nouvelle
        self.assertEqual(str(Quoridor(["foo", "bar"])), nouveau_jeu)
        # Test de création d'une partie déjà existante
        self.assertEqual(str(Quoridor(partie_existante_etat['joueurs'],
                                      partie_existante_etat['murs'])),
                         partie_existante_rootau)
        # Test de l'erreur soulevée si l'argument 'joueur' n'est pas itérable
        self.assertRaisesRegex(QuoridorError, "joueurs n'est pas iterable!", Quoridor, 2)
        # Test de l'erreur soulevée si l'argument 'joueur' n'est pas de longueur 2
        self.assertRaisesRegex(QuoridorError,
                               "Il n'y a pas exactement 2 joueurs!",
                               Quoridor,
                               ["joueur1"])
        self.assertRaisesRegex(QuoridorError,
                               "Il n'y a pas exactement 2 joueurs!",
                               Quoridor,
                               ["joueur1", "joueur2", "joueur3"])
        # Test de l'erreur soulevée si le nombre de murs qu'un joueur peut
        # placer est > 10 ou négatif
        self.assertRaisesRegex(QuoridorError,
                               "mauvais nombre de murs!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 11, "pos": (5, 6)},
                                   {"nom": "bar", "murs": 10, "pos": (5, 7)}
                               ])
        self.assertRaisesRegex(QuoridorError,
                               "mauvais nombre de murs!",
                               Quoridor,
                               [
                                   {"nom": "joueur1", "murs": 10, "pos": (5, 6)},
                                   {"nom": "joueur2", "murs": -1, "pos": (5, 7)}
                               ])
        # Test de l'erreur soulevée si la position d'un joueur est invalide
        self.assertRaisesRegex(QuoridorError,
                               "position du joueur invalide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 10, "pos": (5, 10)},
                                   {"nom": "bar", "murs": 10, "pos": (5, 5)}
                               ])
        self.assertRaisesRegex(QuoridorError,
                               "position du joueur invalide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 10, "pos": (5, 10)},
                                   {"nom": "bar", "murs": 10, "pos": (5, 5)}
                               ])
        # Test de l'erreur soulevée si l'argument "mur" n'est pas un dictionnaire lorsque présent
        self.assertRaisesRegex(QuoridorError,
                               "murs n'est pas un dictionnaire!",
                               Quoridor,
                               ["joueur1", "joueur2"],
                               [(5, 5)])
        # Test de l'erreur soulevée si le total des murs placés et plaçables n'est pas égal à 20
        self.assertRaisesRegex(QuoridorError,
                               "mauvaise quantité totale de murs!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 5, "pos": (5, 6)},
                                   {"nom": "bar", "murs": 10, "pos": (5, 7)}
                               ])
        self.assertRaisesRegex(QuoridorError,
                               "mauvaise quantité totale de murs!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 8, "pos": (5, 6)},
                                   {"nom": "bar", "murs": 3, "pos": (5, 7)}
                               ],
                               {
                                   "horizontaux": [(4, 4), (2, 6), (3, 8), (5, 8), (7, 8)],
                                   "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7)]
                               })
        # Test de l'erreur soulevée si la position d'un mur est invalide
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(0, 5)],
                                   "verticaux": [(5, 5)]
                               })
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(9, 5)],
                                   "verticaux": [(5, 5)]
                               })
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!", Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(5, 1)],
                                   "verticaux": [(5, 5)]
                               })
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!", Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(5, 10)],
                                   "verticaux": [(5, 5)]
                               })
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(5, 5)],
                                   "verticaux": [(1, 5)]
                               })
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(5, 5)],
                                   "verticaux": [(10, 5)]
                               })
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(5, 5)],
                                   "verticaux": [(5, 0)]
                               })
        self.assertRaisesRegex(QuoridorError,
                               "position du mur non-valide!",
                               Quoridor,
                               [
                                   {"nom": "foo", "murs": 9, "pos": (3, 3)},
                                   {"nom": "bar", "murs": 9, "pos": (7, 7)}
                               ],
                               {
                                   "horizontaux": [(5, 5)],
                                   "verticaux": [(5, 9)]
                               })
    def test_déplacer_jeton(self):
        """ Test de la fonction déplacer_jeton
            Cas à tester:
                - déplacement des deux joueurs fonctionne bien
                - QuoridorError si le joueur indiqué est invalide
                - QuoridorError si la position est hors des limites du jeu
                - QuoridorError si la position n'est pas accessible au joueur
        """
        etat_partie = {
            "joueurs": [
                {"nom": "joueur1", "murs": 7, "pos": (5, 6)},
                {"nom": "joueur2", "murs": 3, "pos": (5, 7)}
            ],
            "murs": {
                "horizontaux": [(4, 4), (2, 6), (3, 8), (5, 8), (7, 8)],
                "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7)]
            }}
        etat_partie2 = {
            "joueurs": [
                {"nom": "joueur1", "murs": 7, "pos": (5, 6)},
                {"nom": "joueur2", "murs": 3, "pos": (5, 5)}
            ],
            "murs": {
                "horizontaux": [(4, 4), (2, 6), (3, 8), (5, 8), (7, 8)],
                "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7)]
            }}
        etat_partie3 = {
            "joueurs": [
                {"nom": "joueur1", "murs": 7, "pos": (5, 6)},
                {"nom": "joueur2", "murs": 3, "pos": (6, 5)}
            ],
            "murs": {
                "horizontaux": [(4, 4), (2, 6), (3, 8), (5, 8), (7, 8)],
                "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7)]
            }}
        nouveaujeu = Quoridor(["joueur1", "joueur2"])
        # Tester l'erreur soulevée si le joueur indiqué est invalide
        self.assertRaisesRegex(QuoridorError,
                               "joueur invalide!",
                               nouveaujeu.déplacer_jeton, 5, (5, 2))
        # Tester l'erreur soulevée si la position demandée est hors des limites du jeu
        self.assertRaisesRegex(QuoridorError,
                               "position invalide!",
                               nouveaujeu.déplacer_jeton, 1, (0, 5))
        self.assertRaisesRegex(QuoridorError,
                               "position invalide!",
                               nouveaujeu.déplacer_jeton, 1, (10, 5))
        self.assertRaisesRegex(QuoridorError,
                               "position invalide!",
                               nouveaujeu.déplacer_jeton, 1, (5, 0))
        self.assertRaisesRegex(QuoridorError,
                               "position invalide!",
                               nouveaujeu.déplacer_jeton, 1, (5, 10))
        # Tester l'erreur soulevée si la position demandée n'est pas accessible au joueur
        jeu = Quoridor(etat_partie['joueurs'], etat_partie['murs'])
        self.assertRaisesRegex(QuoridorError,
                               "mouvement invalide!",
                               jeu.déplacer_jeton, 2, (5, 8))
        self.assertRaisesRegex(QuoridorError,
                               "mouvement invalide!",
                               jeu.déplacer_jeton, 1, (5, 8))
        self.assertRaisesRegex(QuoridorError,
                               "mouvement invalide!",
                               jeu.déplacer_jeton, 2, (3, 7))
        self.assertRaisesRegex(QuoridorError,
                               "mouvement invalide!",
                               jeu.déplacer_jeton, 2, (4, 6))
        self.assertRaisesRegex(QuoridorError,
                               "mouvement invalide!",
                               jeu.déplacer_jeton, 2, (6, 6))
        # Tester des déplacements qui fonctionnent
        jeu.déplacer_jeton(2, (5, 5))
        self.assertEqual(jeu.état_partie(), etat_partie2)
        jeu.déplacer_jeton(2, (6, 5))
        self.assertEqual(jeu.état_partie(), etat_partie3)
    def test_état_partie(self):
        """ Test la fonction état_partie
            Cas à tester:
                - La fonction retourne le bon résultat
        """
        nouvelle_partie_etat = {
            "joueurs": [
                {"nom": "joueur1", "murs": 10, "pos": (5, 1)},
                {"nom": "joueur2", "murs": 10, "pos": (5, 9)}
            ],
            "murs": {
                "horizontaux": [],
                "verticaux": []
            }}
        # Tester si la fonction retourne la bonne affichage
        nouvellepartie = Quoridor(["joueur1", "joueur2"])
        self.assertEqual(nouvellepartie.état_partie(), nouvelle_partie_etat)
    def test_jouer_coup(self):
        """ Test la fonction jouer_coup
            Cas à tester:
                - La fonction joue le bon coup automatiquement
                - QuoridorError si le numéro du joueur est invalide
                - QuoridorError si la partie est déjà terminée
        """
        partie_terminee_etat = {
            "joueurs": [
                {"nom": "joueur1", "murs": 7, "pos": (5, 9)},
                {"nom": "joueur2", "murs": 3, "pos": (6, 9)}
            ],
            "murs": {
                "horizontaux": [(4, 4), (2, 6), (3, 8), (5, 8), (7, 8)],
                "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7)]
            }}
        # Tester l'erreur soulevée lorsqu'on donne un joueur invalide
        jeu_nouveau = Quoridor(["joueur1", "joueur2"])
        self.assertRaisesRegex(QuoridorError,
                               "joueur invalide!",
                               jeu_nouveau.jouer_coup, 5)
        # tester l'erreur soulevée l'orsqu'on cherche à jouer un
        # coup alors que la partie est déjà terminée
        jeu_termine = Quoridor(partie_terminee_etat['joueurs'],
                               partie_terminee_etat['murs'])
        self.assertRaisesRegex(QuoridorError,
                               "La partie est déjà terminée!",
                               jeu_termine.jouer_coup, 1)
    def test_partie_terminée(self):
        """ Test de la fonction partie_terminée
            Cas à tester:
                - La fonction retourne False si la partie n'est pas terminée
                - La fonction retourne le nom du joueur qui a gagné si la partie est terminée
        """
        partie_terminee1_etat = {
            "joueurs": [
                {"nom": "joueur1", "murs": 7, "pos": (5, 9)},
                {"nom": "joueur2", "murs": 3, "pos": (6, 9)}
            ],
            "murs": {
                "horizontaux": [(4, 4), (2, 6), (3, 8), (5, 8), (7, 8)],
                "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7)]
            }}
        partie_terminee2_etat = {
            "joueurs": [
                {"nom": "joueur1", "murs": 7, "pos": (6, 1)},
                {"nom": "joueur2", "murs": 3, "pos": (5, 1)}
            ],
            "murs": {
                "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
            }}
        # Tester que la fonction retourne False si la partie n'est pas terminée
        jeu_pas_fini = Quoridor(['joueur1', 'joueur2'])
        self.assertEqual(jeu_pas_fini.partie_terminée(), False)
        # Tester que la fonction retourne le nom du joueur qui a gagné quand c'est le cas
        jeu_fini1 = Quoridor(partie_terminee1_etat['joueurs'], partie_terminee1_etat['murs'])
        self.assertEqual(jeu_fini1.partie_terminée(), "joueur1")
        jeu_fini2 = Quoridor(partie_terminee2_etat['joueurs'], partie_terminee2_etat['murs'])
        self.assertEqual(jeu_fini2.partie_terminée(), "joueur2")
    def test_placer_mur(self):
        """ Test de la fonction placer_mur
            Cas à tester:
                - Les murs horizontaux et verticaux sont placés correctement
                - QuoridorError si le numéro du joueur n'est pas bon
                - QuoridorError si un mur occupe déjà la position
                - QuoridorError si la position est invalide pour l'horientation
                - QuoridorError si le joueur a déjà placé tous ses murs
        """
        jeu1_etat = {
            "joueurs": [
                {"nom": "joueur1", "murs": 9, "pos": (5, 1)},
                {"nom": "joueur2", "murs": 9, "pos": (5, 9)}
            ],
            "murs": {
                "horizontaux": [(4, 4)],
                "verticaux": [(6, 6)]
            }}
        jeu2_etat = {
            "joueurs": [
                {"nom": "joueur1", "murs": 8, "pos": (5, 1)},
                {"nom": "joueur2", "murs": 8, "pos": (5, 9)}
            ],
            "murs": {
                "horizontaux": [(4, 4), (5, 5)],
                "verticaux": [(6, 6), (7, 7)]
            }}
        jeu3_etat = {
            "joueurs": [
                {"nom": "joueur1", "murs": 7, "pos": (5, 3)},
                {"nom": "joueur2", "murs": 0, "pos": (3, 5)}
            ],
            "murs": {
                "horizontaux": [(4, 4), (2, 6), (4, 2), (5, 8), (7, 8)],
                "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7),
                              (2, 2), (2, 3), (2, 4)]
            }}
        jeu1 = Quoridor(jeu1_etat['joueurs'], jeu1_etat['murs'])
        # Tester si le mur est bien placé avec les 2 joueurs
        jeu1.placer_mur(1, (5, 5), 'horizontal')
        jeu1.placer_mur(2, (7, 7), 'vertical')
        self.assertEqual(jeu1.état_partie(), jeu2_etat)
        # Tester l'erreur si le numéro du joueur n'est pas bon
        self.assertRaisesRegex(QuoridorError, "joueur invalide!",
                               jeu1.placer_mur, 5, (2, 2), 'horizontal')
        # Tester l'erreur si le joueur ne peut plus placer de murs
        jeu3 = Quoridor(jeu3_etat['joueurs'], jeu3_etat['murs'])
        self.assertRaisesRegex(QuoridorError, "le joueur ne peut plus placer de murs!",
                               jeu3.placer_mur, 2, (2, 2), 'horizontal')
        # Tester l'erreur si l'emplacement est déjà occupé pour un mur horizontal -->
        # position exacte
        self.assertRaisesRegex(QuoridorError, "Il y a déjà un mur!",
                               jeu3.placer_mur, 1, (4, 4), 'horizontal')
        # Position décallée
        self.assertRaisesRegex(QuoridorError, "Il y a déjà un mur!",
                               jeu3.placer_mur, 1, (5, 4), 'horizontal')
        # Tester l'erreur si l'emplacement est déjà occupé pour un mur vertical --> position exacte
        self.assertRaisesRegex(QuoridorError, "Il y a déjà un mur!",
                               jeu3.placer_mur, 1, (4, 4), 'vertical')
        # Position décallée
        self.assertRaisesRegex(QuoridorError, "Il y a déjà un mur!",
                               jeu3.placer_mur, 1, (4, 5), 'vertical')
        # Tester l'erreur si l'orientation n'est pas valide
        self.assertRaisesRegex(QuoridorError, "orientation invalide!",
                               jeu3.placer_mur, 1, (4, 5), 'diagonale')
        # Tester l'erreur si la position est hors des limites du jeu pour un mur horizontal
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (0, 5), 'horizontal')
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (9, 5), 'horizontal')
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (5, 1), 'horizontal')
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (5, 10), 'horizontal')
        # Tester l'erreur si la position est hors des limites du jeu pour un mur vertical
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (1, 5), 'vertical')
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (10, 5), 'vertical')
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (5, 0), 'vertical')
        self.assertRaisesRegex(QuoridorError, "position du mur invalide!",
                               jeu1.placer_mur, 1, (5, 9), 'vertical')
        # tester l'erreur si le coup enfermerait le joueur
        self.assertRaisesRegex(nx.exception.NetworkXError, "",
                               jeu3.placer_mur, 1, (3, 3), 'horizontal')
        self.assertRaisesRegex(nx.exception.NetworkXError, "",
                               jeu3.placer_mur, 1, (4, 2), 'vertical')
