'''api.py

fonction pour communiquer avec le serveur python
Contient les fonctions:
    - lister_parties (projet)
        Communiquer avec le serveur pour obtenir les 20 dernières parties du joueur
    - débuter_parties (projet)
        communiquer avec le serveur pour demmarer une nouvelle partie et obtenir
        l'etat de la nouvelle table de jeu
    - jouer_coup (projet)
        communiquer avec le serveur pour enregistrer le nouveau coup et obtenir l'etat
        de la table de jeu updatée.
'''
import requests


# URL du server python à contacter
URL_BASE = 'https://python.gel.ulaval.ca/quoridor/api/'

def lister_parties(idul):
    '''def lister_parties(idul)

    Desctiption:
        Fonction qui permet de demander au serveur une liste des
        20 dernières parties jouée par le joueur
    Input:
        idul (str):
            L'identifiant IDUL du joueur
    Return:
        rep (list):
            Une liste des max 20 dernières parties jouées par le joueur
    Note:
        - Si le serveur retourne un message, la fonction soulève une
        exception RuntimeError suivi de ce message.
    '''
    rep = requests.get(URL_BASE+'lister/', params={'idul': idul})
    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        rep = rep.json()
        # tester pour la présence d'un message dans la réponse
        if "message" in rep:
            raise RuntimeError(rep["message"])
    else:
        print(f"Le GET sur {URL_BASE+'lister'} a produit le code d'erreur {rep.status_code}.")
    return rep



def débuter_partie(idul):
    '''def débuter_partie(idul)

    Desctiption:
        Une fonction qui permet de contacter le serveur afin de débuter une partie
    Input:
        idul (str)
            L'identifiant IDUL du joueur
    Return:
        rep (dict)
            Un dictionnaire contenant:
                - 'id' (str):
                    L'identifiant unique de la partie
                - 'état' (dict):
                    Un dictionnaire contenant l'état initial de la partie
    Note:
        - Si le serveur retourne un message, la fonction soulève
            une exception RuntimeError suivi de ce message.
    '''
    rep = requests.post(URL_BASE+'débuter/', data={'idul': idul})
    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        rep = rep.json()
        # tester pour la présence d'un message dans la réponse
        if "message" in rep:
            raise RuntimeError(rep["message"])
    else:
        print(f"Le GET sur {URL_BASE+'lister'} a produit le code d'erreur {rep.status_code}.")
    return rep



def jouer_coup(id_partie, type_coup, position):
    '''def jouer_coup(id, ctype, pos)

    Description:
        Une fonction permettant de contacter le serveur afin de jouer le prochain coup
    Input:
        - id_partie (str):
            L'identifiant unique de la partie
        - type_coup (str):
            le type de coup à jouer:
                - 'D' = Déplacer l'avatar
                - 'MH' = Placer un mur horizontal
                - 'MV' = Placer un mur vertical
        - position (tuple):
            Un tuple (x, y) contenant les coordonnées X et Y où le coup doit s'appliquer
    Return:
        rep (dict):
            Un dictionnaire contenant le nouvel état de la partie
    Notes:
        - Si le serveur retourne un message, la fonction soulève
            une exception RuntimeError suivi de ce message.
        - Si le serveur retour un gagnant, la fonction soulève
            une exception StopInteration suivi du nom du gagnant.
    '''
    rep = requests.post(URL_BASE+'jouer/',
                        data={'id': id_partie,
                              'type': type_coup,
                              'pos': position})
    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        rep = rep.json()
        if 'gagnant' in rep:
            # soulever l'exception
            raise StopIteration(rep["gagnant"])
        # tester pour la présence d'un message dans la réponse
        if "message" in rep:
            raise RuntimeError(rep["message"])
        # tester s'il y a un gagnant
    else:
        print(f"Le GET sur {URL_BASE+'lister'} a produit le code d'erreur {rep.status_code}.")
    return rep
