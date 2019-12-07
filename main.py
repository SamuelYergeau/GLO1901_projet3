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
import quoridor
import quoridorx
import tkinter as tk
from tkinter import simpledialog as sd


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
    
    parser.add_argument('-l', '--lister',
                        dest='lister',
                        action='store_true',
                        help="Lister les identifiants de vos 20 dernières parties.")
    parser.add_argument('-a',
                        dest='auto',
                        action='store_true',
                        help="Jouer en mode automatique contre le serveur avec le nom idul")
    parser.add_argument('-x',
                        dest='graphique',
                        action='store_true',
                        help="Jouer en mode manuel contre le serveur avec le nom idul, " +
                              "mais avec un affichage dans une fenêtre graphique")
    parser.add_argument('-ax',
                        dest='autographique',
                        action='store_true',
                        help="Jouer en mode automatique contre le serveur avec le nom idul, " +
                              "mais avec un affichage dans une fenêtre graphique")
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
        FIXME: l'affichage ne fonctionne plus
    '''
    gamelist = api.lister_parties(idul)
    print("voici la liste de vos 20 dernières parties jouées")
    # itérer sur chaque parties à afficher
    for gamenumber, game in enumerate(gamelist):
        print("partie NO.", gamenumber)
        print("game ID:", game['id'])
        # afficher l'état final du jeu
        #afficher_damier_ascii(game['état'])


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



def jeu_manuel_serveur(idul):
    """mode de jeu permettant de jouer en mode manuel contre le serveur
    - Les commandes sont entrées via le terminal
    - L'affichage s'effectue via le terminal en art ascii    
    Arguments:
        idul {str} -- L'identifiant du joueur
    """
    # débuter le jeu
    nouveaujeu = api.débuter_partie(idul)
    jeu = quoridor.Quoridor(nouveaujeu[1]['joueurs'])
    gameid = nouveaujeu[0]
    jeu.set_mode('server')
    jeu.set_automode('False')
    # afficher le jeu
    print(jeu)

    # boucler
    while True:
        # demander au joueur son prochain coup
        coup = prompt_player()

        # jouer le coup
        try:
            nouveaujeu = api.jouer_coup(gameid, coup[0], (coup[1], coup[2]))
            jeu = quoridor.Quoridor(nouveaujeu['joueurs'], nouveaujeu['murs'])
            print(jeu)
        except quoridor.QuoridorError:
            #jeu = quoridor.Quoridor(nouveaujeu['joueurs'])
            print(jeu)
        except RuntimeError as r:
            print("\nERREUR!: ", r, '\n')
            continue
        except StopIteration as s:
            # prévenir le joueur que la partie est terminée
            print('\n' + '~' * 39)
            print("LA PARTIE EST TERMINÉE!")
            print("LE JOUEUR {} À GAGNÉ!".format(s))
            print('~' * 39 + '\n')
            return



def jeu_auto_serveur(idul):
    """jouer contre le serveur en mode automatique
    - le jeu est géré par le AI
    - l'affichage se fait dans le terminal    
    Arguments:
        idul {str} -- L'identifiant du joueur
    """
    nouveaujeu = api.débuter_partie(idul)
    jeu = quoridor.Quoridor(nouveaujeu[1]['joueurs'])
    jeu.set_id(nouveaujeu[0])
    jeu.set_mode('server')
    jeu.set_automode('True')
    # afficher le jeu
    print(jeu)

    # boucler
    while True:
        # obtenir le prochain coup
        try:
            nouveaujeu = jeu.jouer_coup(1)
            jeu.joueurs = nouveaujeu['joueurs']
            jeu.murh = nouveaujeu['murs']['horizontaux']
            jeu.murv = nouveaujeu['murs']['verticaux']
            print(jeu)
        except quoridor.QuoridorError:
            #jeu.joueurs = nouveaujeu['joueurs']
            print(jeu)
        except StopIteration as si:
            print('gagnant: ', si)
            return



def jeu_manuel_graphique_serveur(idul):
    """jeu manuel affiché dans un interface graphique
    - Les coups sont entrés dans l'interface graphique
    - L'affichage se fait dans l'interface graphique    
    Arguments:
        idul {str} -- L'identifiant du joueur
    """
    nouvellepartie = api.débuter_partie(idul)
    game_id = nouvellepartie[0]
    jeu = quoridorx.QuoridorX(nouvellepartie[1]['joueurs'])

    # set le jeu pour jouer avec le serveur
    jeu.set_mode('server')
    jeu.set_id(game_id)
    tk.mainloop()


def jeu_auto_graphique_serveur(idul):
    """jeu automatique affiché dans un interface graphique
    - Les coup sont gérés par l'AI
    - L'affichage se fait dans l'interface graphique    
    Arguments:
        idul {str} -- L'identifiant du joueur
    """
    nouvellepartie = api.débuter_partie(idul)
    game_id = nouvellepartie[0]
    jeu = quoridorx.QuoridorX(nouvellepartie[1]['joueurs'])

    # set le jeu pour jouer avec le serveur
    jeu.set_mode('server')
    jeu.set_id(game_id)
    jeu.set_automode(True)
    tk.mainloop()    


def jeu_manuel():
    pass


def repartition_options(options):
    """Fonction qui reçois des options de analyser_commande
    et enclanche les mécanismes de jeu en fonction de ces derniers    
    Arguments:
        options {nameplace} -- liste des options dans lesquelles le jeu se déroulera
    """
    # check if more than one option is true
    if sum([options.auto, options.graphique, options.autographique, options.lister]) > 1:
        raise ValueError("too many options chosen!")

    # sent every option to their respective function
    if options.lister:
        pass
    elif options.auto:
        jeu_auto_serveur(options.idul)
    elif options.graphique:
        jeu_manuel_graphique_serveur(options.idul)
    elif options.autographique:
        jeu_auto_graphique_serveur(options.idul)
    else:
        jeu_manuel_serveur(options.idul)

    


if __name__ == "__main__":
    repartition_options(analyser_commande())
    
    

