'''main.py

document principal du jeu quoridor. contient la logique du programme.
Effectue les tâches:
    - recevoir le idul d'un joueur
    - débuter la partie
    - afficher la table de jeu
    - intéragir avec le joueur pour continuer le jeu
    - intéragir avec api.py pour communiquer avec le serveur
Contient les fonctions:
    - afficher_damier_ascii (projet)
        affiche la table de jeu en fonction des informations obtenues du serveur
    - analyser_commande (projet)
        écoute le terminal pour obtenir le idul du joueur et savoir si ce dernier
        souhaire obtenir la liste de ses 20 dernières parties
    - listing (useful tools)
        obtient la liste des 20 dernières parties du joueur et les lui affichent
    - debuter (structure logique)
        effectue les opérations pour débuter une nouvelle partie
    - prompt_player (structure logique)
        intéragit avec le joueur pour obtenir les informations de son prochain coup
    - boucler (structure logique)
        effectue la logique rincipale de la partie:
        - obtenir le prochain coup
        - notifier le serveur
        - afficher le jeu
        - terminer le jeu
'''
import argparse
import api
import quoridorx
import quoridor


# Storer le id
GAME_ID = ''
def afficher_damier_ascii(etat):
    '''def afficher_damier_ascii(etat)

    Desctiprion:
        Une fonction qui construit une visualisation graphique de la table de jeu
        en se basant sur les informations données dans le dictionnaire "etat"
        et l'affiche à la console de commange
    Input:
        etat(dict)
            Un dictionnaire contenant l'état du jeu. contient:
                - {"joueurs": list[dict]} informations sur les joueurs:
                    - {"Nom": str}:  Le nom du joueur
                    - {"murs": int}: Le nombre de murs que le joueur peut encore jouer
                    - {"pos": list}: La position [x, y]* du joueur
                - {"murs": dict}: la position des murs:
                    - {"horizontaux": list}:    Une liste des positions [x, y]* des murs horizontaux
                    - {"verticaux": list}:      Une liste des positions [x, y]* des murs verticaux
                *la position du joueur est relative à la grille VISUELLE du tableau affiché
    Return:
        none
    Note:   ce tableau de jeu est fait en sorte qu'il puisse être configurable.
            Sa taille et son nombre de joueur peuvent donc être changés sans
            impacter la stabilité. Ainsi, des modifications futures seront beaucoup
            plus faciles.
    '''
    # définition des contraintes du tableau de jeu
    # permet de modifier la taille du jeu si désiré
    board_positions = 9
    spacing_horizontal = ((board_positions * 4) - 1)
    # tableaux d'équivalences entre les adresses du jeu et notre tableau
    game_pos_x = range(1, (board_positions * 4), 4)
    game_pos_y = range(((board_positions - 1) * 2), -1, -2)
    # Création du tableau de jeu
    # place holder où ajouter tous les joueurs (pour permettre plus de 2 joueurs)
    légende = "légende: "
    board = [légende]
    # game board
    for i in reversed(range((board_positions * 2) - 1)):
        if (i % 2) == 0:
            board += ["{} |".format(((i + 1) // 2) + 1)]
            board += [' ', '.']
            board += ([' ', ' ', ' ', '.'] * (board_positions - 1))
            board += [' ', '|\n']
        else:
            board += ["  |"]
            board += ([' '] * spacing_horizontal)
            board += ['|\n']
    # bottom board line
    board += "--|" + ('-' * spacing_horizontal) + '\n'
    # bottom number line
    board += (' ' * 2) + '| '
    for i in range(1, board_positions):
        board += str(i) + (' ' * 3)
    board += "9\n"
    # insertion des joueurs dans board
    for num, joueur in enumerate(etat["joueurs"]):
        # ajout du joueur à la légende du tableau
        légende += "{}={} ".format((num + 1), joueur['nom'])
        # obtention de la position en [x, y] du joueur
        position = joueur["pos"]
        # vérification que la position est dans les contraintes
        if ((0 > position[0] > board_positions) or
                (0 > position[1] > board_positions)):
            raise IndexError("Adresse du joueur invalide!")
        # calcul du décallage relatif au tableau
        indice = (game_pos_x[(position[0] - 1)] +
                  (game_pos_y[(position[1] - 1)] * spacing_horizontal))
        decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
        indice += decallage
        # Insérer le personnage dans le tableau de jeu
        board[indice] = str(num + 1)
    # complétion de la légende du tableau
    board[0] = légende + '\n' + (' ' * 3) + ('-' * spacing_horizontal) + '\n'
    # insertion des murs horizontaux dans board
    for murh in etat["murs"]["horizontaux"]:
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
    for murv in etat["murs"]["verticaux"]:
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
    print(''.join(board))


def analyser_commande():
    '''def analyser_commande(commande)
    Description:
        Une fonction qui permet au joueur d'intéragir avec le jeu
        en entrant des commandes dans le terminal
    Input:
        None
    Return:
        Un objet argparse.ArgumentParser contenant la réponse du joueur
    '''
    parser = argparse.ArgumentParser(
        description="Jeu Quoridor - phase 1"
    )
    # indiquer au joueur d'entrer son nom
    parser.add_argument('idul',
                        default='nom_du_joueur',
                        help="IDUL du joueur.")
    parser.add_argument('-l', '--lister',
                        dest='lister',
                        action='store_true',
                        help="Lister les identifiants de vos 20 dernières parties.")
    return parser.parse_args()


def listing(idul):
    '''def listing(idul)
    Description:
        une fonction qui affiche les 20 dernières parties
    Input:
        idul (str)
            le idul du joueur
    Return:
        une liste contenant les réponses du joueur
    '''
    gamelist = api.lister_parties(idul)
    print("voici la liste de vos 20 dernières parties jouées")
    # itérer sur chaque parties à afficher
    for gamenumber, game in enumerate(gamelist['parties']):
        print("partie NO.", gamenumber)
        print("game ID:", game['id'])
        # afficher l'état final du jeu
        afficher_damier_ascii(game['état'])


def debuter(com):
    '''def debuter
    Description:
        accueilles le joueur et affiche le tableau
    Input:
        etat (dict)
            Un dictionnaire contenant les informations sur la table de jeu
    Return:
        le id du jeu
    '''
    # transmettre le idul au serveur et recevoir l'état initial du jeu
    newboard = api.débuter_partie(com.idul)
    # petit mot de bienvenu (tout est dans les détails après tout)
    print('\n' + '~' * 39)
    print("BIENVENU DANS QUORIDOR!")
    print('~' * 39 + '\n')
    # afficher le jeu initial
    afficher_damier_ascii(newboard['état'])
    return newboard['id']


def prompt_player():
    '''def prompt_player()
    Description:
        une fonction qui demande au joueur son prochain coup
    Input:
        None
    Return:
        une liste contenant les réponses du joueur
    '''
    # demander au joueur de jouer son prochain coup
    print("Veuiller jouer votre prochain coup:")
    # demander de spécifier le type de coup
    print("veuiller spécifier le type de coup à jouer:")
    print("    - D :  déplacer votre pion")
    print("    - MH : Poser un mur horizontal")
    print("    - MV : Poser un mur vertical")
    couptype = input("type de coup: ").upper()
    # demander de spécifier la position en X du coup
    print("Veuiller indiquer la position en X de votre coup")
    coupposx = input("position X: ")
    print("veuiller indiquer la position en Y de votre coup")
    coupposy = input("positiony: ")
    return [couptype, coupposx, coupposy]


def boucler():
    '''def boucler()
    Description:
        une fonction qui fait boucler la logique de la partie
    Input:
        None
    Return:
        None
    '''
    while True:
        # demander au joueur de jouer son prochain coup
        nouveaucoup = prompt_player()
        # jouer le coup
        try:
            newboard = api.jouer_coup(GAME_ID, nouveaucoup[0],
                                      (nouveaucoup[1], nouveaucoup[2]))
        except RuntimeError as r:
            print("\nERREUR!: ", r, '\n')
            continue
        except StopIteration as s:
            # prévenir le joueur que la partie est terminée
            print('\n' + '~' * 39)
            print("LA PARTIE EST TERMINÉE!")
            print("LE JOUEUR {} À GAGNÉ!".format(s))
            print('~' * 39 + '\n')
            # afficher l'état final du jeu
            #afficher_damier_ascii(rep['état'])
            return
        # Afficher une nouvelle partie
        print("\nVotre coup à été joué avec succès\n")
        afficher_damier_ascii(newboard['état'])


def loop(joueurs, jeu):
    """loop
        Simple fonction pour tester quoridor.py
        # fonction pour le projet 1
        if __name__ == "__main__":
            #  écouter si le joueur veut commencer une partie
            COM = analyser_commande()
            # vérifier si l'argument lister a été appelé
            if 'lister' in COM and COM.lister:
                # appeler la fonction lister
                listing(COM.idul)
            else:
                # débuter la partie et storer le id de la partie
                GAME_ID += debuter(COM)
                # boucler sur la logique de la partie
                boucler()
    """
    while True:
        # Itérer sur les deux joueurs
        for n in range(1, 3):
            try:
                # afficher le jeu
                print("afficher")
                print(jeu)
                jeu.afficher()
                # jouer le coup du joueur 1
                if joueurs[(n - 1)] == "robot":
                    jeu.jouer_coup(n)
                else:
                    print("tout à {}".format(joueurs[(n-1)]))
                    print("indiquer le type de coup à jouer")
                    tcoup = input("[D, MH ou MH]: ").upper()
                    posx = int(input("position en x du coup: "))
                    posy = int(input("position en y du coup: "))
                    # agir selon le type de coup
                    if tcoup == 'D':
                        jeu.déplacer_jeton(n, (posx, posy))
                    elif tcoup == 'MH':
                        jeu.placer_mur(n, (posx, posy), 'horizontal')
                    elif tcoup == 'MV':
                        jeu.placer_mur(n, (posx, posy), 'vertical')
                    else:
                        print("type de coup invalide")
                        continue
                # tester si la partie est terminer
                gagnant = jeu.partie_terminée()
                if gagnant:
                    print('\n' + '~' * 39)
                    print("LA PARTIE EST TERMINÉE!")
                    print("{} À GAGNÉ!".format(gagnant))
                    print('~' * 39 + '\n')
                    jeu.afficher
                    return
            except quoridor.QuoridorError as qe:
                print(qe)
                continue


if __name__ == "__main__":
    """#  écouter si le joueur veut commencer une partie
    COM = analyser_commande()
    # vérifier si l'argument lister a été appelé
    if 'lister' in COM and COM.lister:
        # appeler la fonction lister
        listing(COM.idul)
    else:
        # débuter la partie et storer le id de la partie
        GAME_ID += debuter(COM)
        # boucler sur la logique de la partie
        boucler()"""
    ETAT_JEU = {
        "joueurs": [
            {"nom": "idul", "murs": 7, "pos": [5, 6]},
            {"nom": "automate", "murs": 3, "pos": [5, 7]}
        ],
        "murs": {
            "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
            "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
        }
    }
    #swag lines
    print('\n' + '~' * 39)
    print("BIENVENU DANS QUORIDOR!")
    print('~' * 39 + '\n')
    # offrir de jouer une nouvelle partie ou reprendre une partie existante
    print("souhaitez vous commencer une nouvelle partie ou continuer une partie existante?")
    print("1 = nouvelle partie | 2 = partie existante")
    CHOIX = int(input("choix: "))
    if CHOIX == 1:
        # obtenir le nom des deux joueurs
        print("veuillez entrer le nom des joueurs:")
        JOUEUR1 = input("nom du joueur1: ")
        JOUEUR2 = input("nom du joueur2: ")
        # demarrer une nouvelle partie
        JEU = quoridorx.QuoridorX([JOUEUR1, JOUEUR2])
        loop([JOUEUR1, JOUEUR2], JEU)
    elif CHOIX == 2:
        JEU = quoridorx.QuoridorX(ETAT_JEU['joueurs'], ETAT_JEU['murs'])
        loop(["joueur1", "joueur2"], JEU)
    else:
        print("choix invalide!")
    
    

