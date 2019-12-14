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
import copy
import tkinter as tk
import networkx as nx
import api
import quoridor
import quoridorx
from tkinter import messagebox as mb


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
    parser.add_argument('-a', '--automatique',
                        dest='auto',
                        action='store_true',
                        help="Activer le mode automatique.")
    parser.add_argument('-x', '--graphique',
                        dest='graphique',
                        action='store_true',
                        help="Activer le mode graphique.")
    parser.add_argument('idul',
                        default='nom_du_joueur',
                        help="IDUL du joueur.")
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
    for gamenumber, game in enumerate(gamelist):
        print("partie NO.", gamenumber)
        print("game ID:", game['id'])
        jeu = quoridor.Quoridor(game['état']['joueurs'],
                                game['état']['murs'])
        print(jeu)


def verifier_validite(jeu, coup):
    """fonction pour vérifier que les coups à jouer sont valides    
    Arguments:
        jeu {[type]} -- [description]
        coup {[type]} -- [description]
    """
    try:
        # vérifier que le coup est légal
        if coup[0] == 'D':
            jeu.déplacer_jeton(1, (int(coup[1]), int(coup[2])))
        elif coup[0] == 'MH':
            jeu.placer_mur(1, (int(coup[1]), int(coup[2])), 'horizontal')
        elif coup[0] == 'MV':
            jeu.placer_mur(1, (int(coup[1]), int(coup[2])), 'vertical')
        else:
            print("coup invalide!")
            return False
        return True
    except (quoridor.QuoridorError,
            nx.exception.NetworkXError,
            nx.exception.NetworkXNoPath) as q:
        print("coup invalide!:", q)
        return False


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
    coupposy = input("position Y: ")
    return [couptype, coupposx, coupposy]


def autocommande(jeu):
    # faire une copie du jeu
    tempjeu = copy.deepcopy(jeu)
    try:
        return tempjeu.jouer_coup(1)
    except quoridor.QuoridorError as qe:
        print("exception inatendue:", qe)


def jeu_console_serveur(idul, automode=False):
    """mode de jeu permettant de jouer en mode manuel contre le serveur
    - Les commandes sont entrées via le terminal
    - L'affichage s'effectue via le terminal en art ascii
    Arguments:
        idul {str} -- L'identifiant du joueur
    """
    # débuter le jeu
    nouveaujeu = api.débuter_partie(idul)
    jeu = quoridor.Quoridor(nouveaujeu[1]['joueurs'])
    jeu.gameid = nouveaujeu[0]
    # afficher le jeu
    print(jeu)
    # boucler
    while True:
        # jouer manuellement ou demander au AI de le coup a joue
        if automode:
            coup = autocommande(jeu)
        else:
            coup = prompt_player()
        # jouer le coup
        try:
            if not verifier_validite(jeu, coup):
                print("coup invalide!")
                print(jeu)
                continue
            nouveaujeu = api.jouer_coup(jeu.gameid, coup[0], (coup[1], coup[2]))
            jeu.joueurs = nouveaujeu['joueurs']
            jeu.murh = nouveaujeu['murs']['horizontaux']
            jeu.murv = nouveaujeu['murs']['verticaux']
            print(jeu)
        except StopIteration as s:
            # prévenir le joueur que la partie est terminée
            print('\n' + '~' * 39)
            print("LA PARTIE EST TERMINÉE!")
            print("LE JOUEUR {} À GAGNÉ!".format(s))
            print('~' * 39 + '\n')
            return


def check_task(jeu, task, automode=False):
    if not automode:
        # Vérifier si une nouvelle tâche a été entrée
        if task != jeu.task:
            return jeu.task
    else:
        murs = {'horizontaux':jeu.murh,
                'verticaux':jeu.murv}
        qjeu = quoridor.Quoridor(jeu.joueurs, murs)
        return autocommande(qjeu)


def jeu_graphique_serveur(idul, automode=False):
    """jeu manuel affiché dans un interface graphique
    - Les coups sont entrés dans l'interface graphique
    - L'affichage se fait dans l'interface graphique
    Arguments:
        idul {str} -- L'identifiant du joueur
    """
    # débuter le jeu
    nouveaujeu = api.débuter_partie(idul)
    jeu = quoridorx.QuoridorX(nouveaujeu[1]['joueurs'])
    jeu.gameid = nouveaujeu[0]
    coup = []
    # boucler
    while True:
        # Obtenir le coup
        t = check_task(jeu, coup, automode)
        if t:
            try:
                coup = t
                # vérifier si le coup est valide
                if not verifier_validite(jeu, coup):
                    mb.showerror("Erreur!", "Coup invalide!")
                    continue
                nouveaujeu = api.jouer_coup(jeu.gameid, coup[0], (coup[1], coup[2]))
                jeu.joueurs = nouveaujeu['joueurs']
                jeu.murh = nouveaujeu['murs']['horizontaux']
                jeu.murv = nouveaujeu['murs']['verticaux']
                # Afficher le jeu
                jeu.afficher()
            except StopIteration as s:
                # prévenir le joueur que la partie est terminée
                mb.showinfo("Partie terminée!", f"Le joueur {s} à gagné!")
                return
        # Boucler et continuellement afficher
        jeu.root.update_idletasks()
        jeu.root.update()


def repartition_options(options):
    """Fonction qui reçois des options de analyser_commande
    et enclanche les mécanismes de jeu en fonction de ces derniers
    Arguments:
        options {nameplace} -- liste des options dans lesquelles le jeu se déroulera
    """
    # sent every option to their respective function
    if options.auto and options.graphique:
        jeu_graphique_serveur(options.idul, True)
    elif options.auto:
        jeu_console_serveur(options.idul, True)
    elif options.graphique:
        jeu_graphique_serveur(options.idul)
    else:
        jeu_console_serveur(options.idul)


if __name__ == "__main__":
    repartition_options(analyser_commande())
