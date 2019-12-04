""" Quoridor.py
Module qui enferme les classes d'encapsulation
de la structure du jeu
contient les classes:
    - Quoridor
    - QuoridorError(Exception)
"""
import unittest
import copy
import networkx as nx
import random


def graphe_helper(murs_horizontaux, murs_verticaux):
    """fonction pour aider la fonction construire_graphe
        avec son problème de trop de branches
        Simple fonction de segmentation
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    return graphe


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = graphe_helper(murs_horizontaux, murs_verticaux)

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class QuoridorError(Exception):
    """QuoridorError
    Classe pour gérer les exceptions survenue dans la classe Quoridor
    Arguments:
        Exception {[type]} -- [description]
    """


def check_type(t, variable, message):
    """Simple fonction pour vérifier le type d'une variable
        Sers simplement à alléger les fonctions qui ont un
        trop de branches
    Arguments:
        type {[type]} -- le type de variable à tester
        variable {} -- la variable en question
        message {String} -- le message à soulever si la faux
    """
    if not isinstance(variable, t):
        raise QuoridorError(message)


def check_iterable(j):
    """Simple fonction pour alléger le nombre
    de branches de __init__
    """
    try:
        iter(j)
    except TypeError:
        raise QuoridorError("joueurs n'est pas iterable!")
    if len(j) != 2:
        raise QuoridorError("Il n'y a pas exactement 2 joueurs!")


def check_total_murs(joueurs, murs):
    """Fonction pour vérifier à la place de __init__ si
    le nombre total de murs donne 20
    Arguments:
        joueurs {[type]} -- [description]
        murs {[type]} -- [description]
    """
    murh = 0
    murv = 0
    murj1 = 0
    murj2 = 0
    # Vérifier s'il y a des murs
    if murs:
        # s'assurer qu'il s'agit bien d'un citctionnaire
        check_type(dict, murs, "murs n'est pas un dictionnaire!")
        murh = len(murs['horizontaux'])
        murv = len(murs['verticaux'])
    # vérifier que joueurs est valide
    check_iterable(joueurs)
    if isinstance(joueurs[0], dict):
        # vérifier que les murs sont legit
        for joueur in joueurs:
            if  not 0 <= joueur['murs'] <= 10:
                raise QuoridorError("mauvais nombre de murs!")
        murj1 = joueurs[0]['murs']
        murj2 = joueurs[1]['murs']
    elif isinstance(joueurs[0], str):
        murj1 = 10
        murj2 = 10
    else:
        raise QuoridorError("joueurs n'est ni des dictionnaires ni des string!")
    if (murh + murv + murj1 + murj2) != 20:
        print("\nmauvaise qt de murs:")
        raise QuoridorError("mauvaise quantité totale de murs!")


class Quoridor:
    """class quoridor"""

    def __init__(self, joueurs, murs=None):
        """
        __init__
        Initialisation de la classe Quoridor
        Arguments:
            joueurs {list}
                -- Une liste de 2 joueurs. chaque joueur est: (dict) ou (str)
                    - (str): nom du joueur
                    - (dict)
                        + 'nom' (str)   -- Nom du joueur
                        + 'murs' (int)  -- Nombre de murs que le joueur peut encore placer
                        + 'pos' (tuple) -- position (x, y) du joueur
        Keyword Arguments:
            murs {dict} (default: {None})
            -- 'horzontaux': [list of tuples]
                Une liste de tuples (x, y) représentant la position des différents
                murs horizontaux dans la partie
        """
        # définir les attribut de classes que nous allons utiliser
        self.joueurs = [{'nom':'', 'murs': 0, 'pos':(0, 0)},
                        {'nom':'', 'murs': 0, 'pos':(0, 0)}]
        self.murh = []
        self.murv = []
        starting_position = [(5, 1), (5, 9)]
        #faire un copie profonde de ce qui a besoin d'être copié
        cjoueurs = copy.deepcopy(joueurs)
        cmurs = copy.deepcopy(murs)
        # Vérifier si le nombre totab de murs donne 20
        check_total_murs(cjoueurs, cmurs)
        # vérifier si un dictionnaire de murs est présent
        if murs:
            # vérifier si murs est un tuple
            check_type(dict, cmurs, "murs n'est pas un dictionnaire!")
            # itérer sur chaque mur horizontal
            for mur in cmurs['horizontaux']:
                # Vérifier si la position du mur est valide
                if not 1 <= mur[0] <= 8 or not 2 <= mur[1] <= 9:
                    raise QuoridorError("position du mur non-valide!")
                self.murh += [tuple(mur)]
            # itérer sur chaque mur vertical
            for mur in cmurs['verticaux']:
                if not 2 <= mur[0] <= 9 or not 1 <= mur[1] <= 8:
                    raise QuoridorError("position du mur non-valide!")
                self.murv += [tuple(mur)]
        # vérifier que joueurs est itérable et de longueur 2
        check_iterable(cjoueurs)
        # itérer sur chaque joueur
        for numero, joueur in enumerate(cjoueurs):
            # Vérifier s'il s'agit d'un string ou d'un dictionnaire
            if isinstance(joueur, str):
                # ajouter le nom au dictionnaire
                self.joueurs[numero]['nom'] = joueur
                # ajouter 10 murs à placer au joueur
                self.joueurs[numero]['murs'] = 10
                # placer le joueur au bon endroit sur le jeu
                self.joueurs[numero]['pos'] = starting_position[numero]
            else:
                # vérifier que les murs sont legit
                if  not 0 <= joueur['murs'] <= 10:
                    raise QuoridorError("mauvais nombre de murs!")
                # Vérifier que la position du joueur est valide
                if not 1 <= joueur['pos'][0] <= 9 or not 1 <= joueur['pos'][1] <= 9:
                    raise QuoridorError("position du joueur invalide!")
                # updater la valeur de joueur
                self.joueurs[numero] = joueur
                # vérifier que la position du joueur est storée comme tuple
                self.joueurs[numero]['pos'] = tuple(self.joueurs[numero]['pos'])


    def __str__(self):
        """
        __str__
        Produit la représentation en art ascii correspondant à l'état actuel de la partie
        Returns:
            board (str)
                Une représentation en art ascii de la root de jeu
        """
        # définition des contraintes du rootau de jeu
        # permet de modifier la taille du jeu si désiré
        board_positions = 9
        spacing_horizontal = ((board_positions * 4) - 1)
        # rootaux d'équivalences entre les adresses du jeu et notre rootau
        game_pos_x = range(1, (board_positions * 4), 4)
        game_pos_y = range(((board_positions - 1) * 2), -1, -2)
        # Création du rootau de jeu
        # en-tête
        board = [
            "légende: 1={} 2={}\n".format(self.joueurs[0]['nom'], self.joueurs[1]['nom']) +
            (' ' * 3) + ('-' * spacing_horizontal) + '\n'
        ]
        # game board
        for i in reversed(range((board_positions * 2) - 1)):
            if (i % 2) == 0:
                # check if more than 10 positions for better formatting
                board += ["{}{}|".format((((i + 1) // 2) + 1),
                                         (' ' * (1 - ((((i + 1) // 2) + 1) // 10))))]
                board += [' ', '.']
                board += ([' ', ' ', ' ', '.'] * (board_positions - 1))
                board += [' ', '|\n']
            else:
                board += ["  |"]
                board += ([' '] * spacing_horizontal)
                board += ['|\n']
        # bottom lines
        board += "--|" + ('-' * spacing_horizontal) + '\n'
        board += (' ' * 2) + '| '
        for i in range(1, board_positions):
            board += str(i) + (' ')
            board += (' ' * (2 - (i // 10)))
        board += "{}\n".format(board_positions)
        # insertion des joueurs dans board
        for num, joueur in enumerate(self.joueurs):
            # obtention de la position en [x, y] du joueur
            position = joueur["pos"]
            # vérification que la position est dans les contraintes
            if ((0 > position[0] > board_positions) or
                    (0 > position[1] > board_positions)):
                raise IndexError("Adresse du joueur invalide!")
            # calcul du décallage relatif au rootau
            indice = (game_pos_x[(position[0] - 1)] +
                      (game_pos_y[(position[1] - 1)] * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            # Insérer le personnage dans le rootau de jeu
            board[indice] = str(num + 1)
        # insertion des murs horizontaux dans board
        for murh in self.murh:
            # vérification que la position est dans les contraintes
            if ((1 > murh[0] > (board_positions - 1)) or
                    (2 > murh[1] > board_positions)):
                raise IndexError("Position du mur horizontal invalide!")
            indice = ((game_pos_x[(murh[0] - 1)] - 1) +
                      ((game_pos_y[(murh[1] - 1)] + 1) * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            # itérer pour placer les 5 murs
            for i in range(7):
                board[(indice + i)] = '-'
        # insertion des murs verticaux
        for murv in self.murv:
            # vérification que la position est dans les contraintes
            if (2 > murv[0] > board_positions) or (1 > murv[1] > board_positions):
                raise IndexError("Position du mur vertical invalide!")
            indice = ((game_pos_x[(murv[0] - 1)] - 2) +
                      (game_pos_y[(murv[1] - 1)] * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            # itérer pour placer les 3 murs
            for i in range(3):
                board[(indice - (i * (spacing_horizontal + 2)))] = '|'
        # afficher le jeu sous forme d'une chaine de caractères
        return ''.join(board)


    def déplacer_jeton(self, joueur, position):
        """
        déplacer_jeton
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée
        Arguments:
            joueur (int): 1 ou 2
            position (tuple):
                Le tuple (x, y) de la position où déplacer le jeton
        Return: None
        """
        # Vérifier que le joueur est valide
        if joueur not in (1, 2):
            raise QuoridorError("joueur invalide!")
        # Vérifier que la position du joueur est valide
        if not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9:
            raise QuoridorError("position invalide!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        # vérifier si le mouvement est valide
        if position not in list(graphe.successors((self.joueurs[(joueur - 1)]['pos']))):
            raise QuoridorError("mouvement invalide!")
        # Changer la position du joueur
        self.joueurs[(joueur - 1)]['pos'] = position


    def état_partie(self):
        """
        état_partie
        Produit l'état actuel du jeu sous la forme d'un dictionnaire
        Arguments: None
        Return:
            une copie de l'état actuel du jeu sous la forme d'un dictionnaire
            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ]
                'Murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }
        """
        return {"joueurs": self.joueurs,
                "murs":{
                    "horizontaux": self.murh,
                    "verticaux": self.murv
                    }}


    def jouer_coup(self, joueur):
        """
        jouer_coup
        Pour le joueur spécifié, jouer automatiquement son meilleur
        coup pour l'état actuel de la partie. Ce coup est soit le déplacement de son jeton,
        soit le placement d'un mur horizontal ou vertical.
        Arguments:
            joueur {int} -- un entier spécifiant le numéro du joueur (1 ou 2)
        NOTE: version temporaire et stupide! à optimiser!
        Return: None
        """
        # objectifs
        objectifs = ['B1', 'B2']
        # Vérifier que le joueur est valide
        if joueur not in (1, 2):
            raise QuoridorError("joueur invalide!")
        # Vérifier si la partie est déjà terminée
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        coup_a_jouer = nx.shortest_path(graphe,
                                        self.joueurs[(joueur - 1)]['pos'],
                                        objectifs[(joueur - 1)])[1]
        # jouer le coup
        self.déplacer_jeton(joueur, coup_a_jouer)

        """SECTION STRATÉGIE DE JEU"""
        # 1) Utililiser le hasard pour décider qu'elle mouvement faire
        # Obtenir un élément au hasard 
        listedescoup = [] 
        if len(listedescoup) <= 0 : 
            poids = [10, 10, 10]
            ma_liste = ["D", "MH", "MV"]
            elem = random.choices(ma_liste,weights=poids)
            listedescoup.append(elem)

        #2) Variez la probabilité de choisir le placement d'un mur en fonction du nombre de murs qui restent à placer.
        murplacer = 0
        for frequence in listedescoup:
            if frequence == "MH" or "MV":
                murplacer += 1
        else:
            poids = [10, 10-murplacer, 10-murplacer]
            ma_liste = ["D", "MH", "MV"]
            elem = random.choices(ma_liste,weights=poids)
            listedescoup.append(elem)




    def partie_terminée(self):
        """
        partie_terminée
        Évalue si la partie est terminée
        Arguments: None
        Return: le nom du joueur si un joueur a gagné. Sinon False
        """
        # definir les conditions de victoire
        condition_de_victoire = [9, 1]
        # itérer sur chaque joueurs
        for numero, joueur in enumerate(self.joueurs):
            # Vérifier si le joueur rempli les conditions de victoires
            if joueur['pos'][1] == condition_de_victoire[(numero)]:
                # Retourner le nom du joueur gagnant
                return joueur['nom']
        return False


    def check_position(self, position):
        """simple fonction pour alléger le nombre
        de branches dans placer_mur
        """
        # vérifier si les positions sont dans les limites du jeu
        if not 1 <= position[0] <= 8 or not 2 <= position[1] <= 9:
            raise QuoridorError("position du mur invalide!")
        # vérifier si l'emplacement est déjà occupé
        if (position[0], position[1]) in self.murh:
            raise QuoridorError("Il y a déjà un mur!")
        # Prendre en compte le décalage des murs
        if ((position[0] - 1), position[1]) in self.murh:
            raise QuoridorError("Il y a déjà un mur!")


    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        """
        placer_mur
        pour le joueur spécifié, placer un mur à la position spécifiée
        Arguments:
            joueur {int} -- Le numéro du joueur (1 ou 2)
            position {tuple} -- le tuple (x, y) de la position du mur
            orientation {str} -- l'orientation du mur: 'horizontal' ou 'vertical'
        Return: None
        """
        # définir les objectifs de chaque joueurs
        objectif = ['B1', 'B2']
        # Vérifier que le joueur est valide
        if joueur not in (1, 2):
            raise QuoridorError("joueur invalide!")
        # Vérifier si le joueur ne peut plus placer de murs
        if self.joueurs[(joueur - 1)]['murs'] <= 0:
            raise QuoridorError("le joueur ne peut plus placer de murs!")
        # Si le mur est horizontal
        if orientation == 'horizontal':
            self.check_position(position)
            # créer un graphe des mouvements possible à jouer avec le mur ajouté
            graphe = construire_graphe(
                [joueur['pos'] for joueur in self.joueurs],
                (self.murh + [position]),
                self.murv
            )
            # vérifier si placer ce mur enfermerais un joueur
            for i in range(2):
                if not nx.has_path(graphe, (self.joueurs[i]['pos']), objectif[i]):
                    raise QuoridorError("ce coup enfermerait un joueur")
            # placer le mur
            self.murh += [position]
            # retirer un mur des murs plaçables du joueurs
            self.joueurs[(joueur - 1)]['murs'] -= 1
        # Si c'est un mur vertical
        elif orientation == 'vertical':
            # vérifier si les positions sont dans les limites du jeu
            if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                raise QuoridorError("position du mur invalide!")
            # vérifier si l'emplacement est déjà occupé
            if (position[0], position[1]) in self.murv:
                raise QuoridorError("Il y a déjà un mur!")
            # Prendre en compte le décalage des murs
            if (position[0], (position[1] - 1)) in self.murv:
                raise QuoridorError("Il y a déjà un mur!")
            # créer un graphe des mouvements possible à jouer avec le mur ajouté
            graphe = construire_graphe(
                [joueur['pos'] for joueur in self.joueurs],
                self.murh,
                (self.murv + [position])
            )
            # vérifier si placer ce mur enfermerais le joueur
            for i in range(2):
                if not nx.has_path(graphe, (self.joueurs[i]['pos']), objectif[i]):
                    raise QuoridorError("ce coup enfermerait un joueur")
            # placer le mur
            self.murv += [position]
            # retirer un mur des murs plaçables du joueurs
            self.joueurs[(joueur - 1)]['murs'] -= 1
        # Si l'orientation n'est ni horizontal ni vertical, soulever une exception
        else:
            raise QuoridorError("orientation invalide!")


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


#Lancer la batterie de tests unitaires l'orsque ce module est lancé en tant que main (pas importé)
if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
