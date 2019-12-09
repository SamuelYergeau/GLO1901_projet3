"""quoridor.py
Module pour contenir la classe QuoridorX
"""
import tkinter as tk
import networkx as nx
import copy
from tkinter import messagebox as mb
import quoridor
import api


class QuoridorX(quoridor.Quoridor):
    '''class quoridorX pour implanter le mode graphique, herite de quoridor'''

    def __init__(self, joueurs, murs=None):
        """initialisation de l'affichage du jeu
        Arguments:
            joueurs {[type]} -- [description]
        Keyword Arguments:
            murs {[type]} -- [description] (default: {None})
        NOTE: améliorer le look de absolument tout
        NOTE: rendre toutes les grandeurs scalables avec les fenêtres
        """
        super().__init__(joueurs, murs)
        self.root = tk.Tk()
        self.root.lift()
        #self.posjoueurs = [self.joueurs[0]['pos'], self.joueurs[1]['pos']]
        self.oldjoueurs = copy.deepcopy(self.joueurs)
        self.nombremurh = len(self.murh)
        self.nombremurv = len(self.murv)
        self.murholders = [0, 0]
        self.playerturn = 1
        self.highlightthickness = 5
        # lists of equivalent positions
        game_pos_x = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]
        game_pos_y = [0, 17, 15, 13, 11, 9, 7, 5, 3, 1]
        game_pos_mur = [0, 2, 4, 6, 8, 10, 12, 14, 16]
        # sizes of the different labels [height, width]
        case_jeu_dimensions = [3, 3]
        mur_h_dimensions = [3, 1]
        mur_v_dimensions = [1, 3]
        # make row labels
        for r in range(1, 10):
            tk.Label(self.root,
                     text=str(10-r)).grid(row=(3 + ((r - 1) * 2)),
                                          column=1)

        # Make column labels
        for r in range(1, 10):
            tk.Label(self.root,
                     width=3,
                     height=1,
                     text=str(r)).grid(row=20,
                                       column=(2 * r))

        # Afficher les murs que chaque joueurs peuvent encore placer
        for num, r in enumerate([23, 2]):
            # Murs des 2 joueurs
            tk.Label(self.root,
                     text="Joueur {} = {}".format((num + 1), self.joueurs[num]['nom']),
                     height=1).grid(column=10, row=(r - 1))
            self.murholders[num] = tk.Frame(self.root,
                                            background='grey',
                                            borderwidth=2,
                                            relief=tk.FLAT)
            self.murholders[num].grid(column=2,
                                      columnspan=17,
                                      row=r,
                                      rowspan=1,
                                      sticky='n')
            for jmurs in range(2, (self.joueurs[(num)]['murs'] + 2)):
                tk.Label(self.murholders[num],
                         width=mur_v_dimensions[0],
                         height=mur_v_dimensions[1],
                         borderwidth=3,
                         relief=tk.RIDGE,
                         padx=5,
                         background='grey',
                         text='').grid(column=jmurs, row=1)

        # Construction du tableau de jeu
        self.board = tk.Frame(self.root,
                              background='brown',
                              borderwidth=2,
                              relief=tk.RIDGE)
        self.board.grid(column=2,
                        columnspan=17,
                        row=3,
                        rowspan=17,
                        sticky='n')
        # dresser la table de jeu
        for i in range(1, 18):
            for j in range(1, 18):
                # Cases de jeu principales
                for numero, joueur in enumerate(self.joueurs):
                    if (game_pos_x[joueur['pos'][0]], game_pos_y[joueur['pos'][1]]) == (i, j):
                        l = tk.Label(self.board,
                                     width=case_jeu_dimensions[0],
                                     height=case_jeu_dimensions[1],
                                     relief=tk.FLAT,
                                     borderwidth=1,
                                     takefocus=True,
                                     highlightcolor='red',
                                     activeforeground='blue',
                                     activebackground='#ffcc99',
                                     highlightthickness=self.highlightthickness,
                                     background='#ffcc99',
                                     text=str(numero + 1))
                        l.grid(row=j, column=i)
                        l.extra = joueur['pos']
                        l.bind("<Button-1>", self.bouger_joueur)
                        l.bind("<Enter>", self.hilight)
                        l.bind("<Leave>", self.unhilight)
                        break
                    else:
                        if (i in game_pos_x) and (j in game_pos_y):
                            l = tk.Label(self.board,
                                         width=case_jeu_dimensions[0],
                                         height=case_jeu_dimensions[1],
                                         relief=tk.FLAT,
                                         borderwidth=1,
                                         takefocus=True,
                                         highlightcolor='blue',
                                         highlightthickness=self.highlightthickness,
                                         activeforeground='blue',
                                         activebackground='#f9f9eb',
                                         background='#f9f9eb',
                                         text='')
                            l.grid(row=j, column=i)
                            l.extra = (game_pos_x.index(i),
                                       game_pos_y.index(j))
                            l.bind("<Button-1>", self.bouger_joueur)
                            l.bind("<Enter>", self.hilight)
                            l.bind("<Leave>", self.unhilight)
                # Murs horizontaux
                if len(self.murh) > 0:
                    for wallh in self.murh:
                        if (game_pos_x[wallh[0]], game_pos_y[wallh[1]]) == (i, (j - 1)):
                            tk.Label(self.board,
                                     width=mur_h_dimensions[0],
                                     height=mur_h_dimensions[1],
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     activeforeground='blue',
                                     activebackground='grey',
                                     highlightthickness=self.highlightthickness,
                                     background='grey',
                                     text='').grid(row=j, column =i)
                            # remplissage de la case vide
                            tk.Label(self.board,
                                     width=1,
                                     height=1,
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     highlightthickness=self.highlightthickness,
                                     background='grey',
                                     text='').grid(row=j, column=(i + 1))
                            break
                        # décallage: x + 1
                        elif (game_pos_x[(wallh[0] + 1)], game_pos_y[wallh[1]]) == (i, (j - 1)):
                            tk.Label(self.board,
                                     width=mur_h_dimensions[0],
                                     height=mur_h_dimensions[1],
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     highlightthickness=self.highlightthickness,
                                     background='grey',
                                     text='').grid(row=j, column=i)
                            break
                        else:
                            if (i in game_pos_x) and (j in game_pos_mur):
                                l = tk.Label(self.board,
                                             width=mur_h_dimensions[0],
                                             height=mur_h_dimensions[1],
                                             background='brown',
                                             borderwidth=1,
                                             relief=tk.FLAT,
                                             takefocus=True,
                                             highlightcolor='blue',
                                             activeforeground='blue',
                                             activebackground='brown',
                                             highlightthickness=self.highlightthickness,
                                             text='')
                                l.grid(row=j, column=i)
                                l.extra = (game_pos_x.index(i),
                                           game_pos_y.index(j - 1))
                                l.bind("<Button-1>", self.placer_murh)
                                l.bind("<Enter>", self.hilight)
                                l.bind("<Leave>", self.unhilight)
                else:
                    if (i in game_pos_x) and (j in game_pos_mur):
                        l = tk.Label(self.board,
                                     width=mur_h_dimensions[0],
                                     height=mur_h_dimensions[1],
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     activeforeground='blue',
                                     activebackground='brown',
                                     highlightthickness=self.highlightthickness,
                                     background='brown',
                                     text='')
                        l.grid(row=j, column=i)
                        l.extra = (game_pos_x.index(i),
                                   game_pos_y.index(j - 1))
                        l.bind("<Button-1>", self.placer_murh)
                        l.bind("<Enter>", self.hilight)
                        l.bind("<Leave>", self.unhilight)
                #Murs verticaux
                if len(self.murv) > 0:
                    for wallv in self.murv:
                        if (game_pos_x[wallv[0]], game_pos_y[wallv[1]]) == ((i + 1), j):
                            tk.Label(self.board,
                                     width=mur_v_dimensions[0],
                                     height=mur_v_dimensions[1],
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     highlightthickness=self.highlightthickness,
                                     background='grey',
                                     text='').grid(row=j, column=i)
                            # remplissage de la case vide
                            tk.Label(self.board,
                                     width=1,
                                     height=1,
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     highlightthickness=self.highlightthickness,
                                     background='grey',
                                     text='').grid(row=(j - 1), column=i)
                            break
                        # décallage: y + 1
                        elif (game_pos_x[wallv[0]], game_pos_y[(wallv[1] + 1)]) == ((i + 1), j):
                            tk.Label(self.board,
                                     width=mur_v_dimensions[0],
                                     height=mur_v_dimensions[1],
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     highlightthickness=self.highlightthickness,
                                     background='grey',
                                     text='').grid(row=j, column=i)
                            break
                        else:
                            if (i in game_pos_mur) and (j in game_pos_y):
                                l = tk.Label(self.board,
                                             width=mur_v_dimensions[0],
                                             height=mur_v_dimensions[1],
                                             borderwidth=1,
                                             relief=tk.FLAT,
                                             takefocus=True,
                                             highlightcolor='blue',
                                             activeforeground='blue',
                                             activebackground='brown',
                                             highlightthickness=self.highlightthickness,
                                             background='brown',
                                             text=' ')
                                l.grid(row=j, column=i)
                                l.extra = (game_pos_x.index(i + 1),
                                           game_pos_y.index(j))
                                l.bind("<Button-1>", self.placer_murv)
                                l.bind("<Enter>", self.hilight)
                                l.bind("<Leave>", self.unhilight)
                else:
                    if (i in game_pos_mur) and (j in game_pos_y):
                        l = tk.Label(self.board,
                                     width=mur_v_dimensions[0],
                                     height=mur_v_dimensions[1],
                                     borderwidth=1,
                                     relief=tk.FLAT,
                                     takefocus=True,
                                     highlightcolor='blue',
                                     activeforeground='blue',
                                     activebackground='brown',
                                     highlightthickness=self.highlightthickness,
                                     background='brown',
                                     text='')
                        l.grid(row=j, column=i)
                        l.extra = (game_pos_x.index(i + 1),
                                   game_pos_y.index(j))
                        l.bind("<Button-1>", self.placer_murv)
                        l.bind("<Enter>", self.hilight)
                        l.bind("<Leave>", self.unhilight)


    def set_automode(self, automode):
        """Setter pour automode
        Set automode à True et demarre le timer
        Arguments:
            automode {bool} -- automode state
        """
        self.automode = automode
        if self.automode == True:
            self.root.after(75, self.auto_play)


    def auto_play(self):
        """Handler pour jouer en mode automatique
        """
        try:
            nouveaujeu = self.jouer_coup(1)
            self.joueurs = nouveaujeu['joueurs']
            self.murh = nouveaujeu['murs']['horizontaux']
            self.murv = nouveaujeu['murs']['verticaux']
            self.afficher()
        except quoridor.QuoridorError:
            self.afficher()
        except StopIteration as si:
            mb.showinfo("Fin de partie",
                        "le joueur {} a gagné la partie!".format(si))
            return
        if self.automode == True:
            self.root.after(75, self.auto_play)


    def afficher(self):
        """met à jours l'affichage
        """
        # lists of equivalent positions
        game_pos_x = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]
        game_pos_y = [0, 17, 15, 13, 11, 9, 7, 5, 3, 1]
        # sizes of the different labels [height, width]
        case_jeu_dimensions = [3, 3]
        mur_h_dimensions = [3, 1]
        mur_v_dimensions = [1, 3]
        # vérifier si le joueur a bougé
        for i in range(2):
            if self.oldjoueurs[i]['pos'] != self.joueurs[i]['pos']:
                #effacer l'ancienne position du joueur
                l = tk.Label(self.board,
                             width=case_jeu_dimensions[0],
                             height=case_jeu_dimensions[1],
                             borderwidth=1,
                             relief=tk.FLAT,
                             takefocus=True,
                             highlightcolor='blue',
                             activeforeground='blue',
                             activebackground='#f9f9eb',
                             highlightthickness=self.highlightthickness,
                             background='#f9f9eb',
                             text='')
                l.grid(row=game_pos_y[self.oldjoueurs[i]['pos'][1]],
                       column=game_pos_x[self.oldjoueurs[i]['pos'][0]])
                l.extra = self.oldjoueurs[i]['pos']
                l.bind("<Button-1>", self.bouger_joueur)
                l.bind("<Enter>", self.hilight)
                l.bind("<Leave>", self.unhilight)
                self.oldjoueurs[i]['pos'] = self.joueurs[i]['pos']
                l = tk.Label(self.board,
                             width=case_jeu_dimensions[0],
                             height=case_jeu_dimensions[1],
                             borderwidth=1,
                             relief=tk.FLAT,
                             takefocus=True,
                             highlightcolor='blue',
                             highlightthickness=self.highlightthickness,
                             activeforeground='blue',
                             activebackground='#ffcc99',
                             background='#ffcc99',
                             text=str(i + 1))
                l.grid(row=game_pos_y[self.oldjoueurs[i]['pos'][1]],
                       column=game_pos_x[self.oldjoueurs[i]['pos'][0]])
                l.extra = self.oldjoueurs[i]['pos']
                l.bind("<Button-1>", self.bouger_joueur)
                l.bind("<Enter>", self.hilight)
                l.bind("<Leave>", self.unhilight)

        # Vérifier si des murs horizontaux ont été placés
        if self.nombremurh < len(self.murh):
            for i in range(2):
                tk.Label(self.board,
                         width=mur_h_dimensions[0],
                         height=mur_h_dimensions[1],
                         borderwidth=1,
                         relief=tk.FLAT,
                         takefocus=True,
                         highlightcolor='blue',
                         highlightthickness=self.highlightthickness,
                         background='grey',
                         text='').grid(row=(game_pos_y[self.murh[-1][1]] + 1),
                                       column=(game_pos_x[self.murh[-1][0]] + (2 * i)))
            # Remplissage de la case vide
            tk.Label(self.board,
                     width=1,
                     height=1,
                     borderwidth=1,
                     relief=tk.FLAT,
                     takefocus=True,
                     highlightcolor='blue',
                     highlightthickness=5,
                     background='grey',
                     text='').grid(row=(game_pos_y[self.murh[-1][1]] + 1),
                                   column=(game_pos_x[self.murh[-1][0]] + 1))
            self.nombremurh = len(self.murh)

        # Vérifier si des murs verticaux ont été placés
        if self.nombremurv < len(self.murv):
            for i in range(2):
                tk.Label(self.board,
                         width=mur_v_dimensions[0],
                         height=mur_v_dimensions[1],
                         borderwidth=1,
                         relief=tk.FLAT,
                         takefocus=True,
                         highlightcolor='blue',
                         highlightthickness=self.highlightthickness,
                         background='grey',
                         text='').grid(row=(game_pos_y[self.murv[-1][1]] - (2 * i)),
                                       column=(game_pos_x[self.murv[-1][0]] - 1))
            # Remplissage de la case vide
            tk.Label(self.board,
                     width=1,
                     height=1,
                     borderwidth=1,
                     relief=tk.FLAT,
                     takefocus=True,
                     highlightcolor='blue',
                     highlightthickness=self.highlightthickness,
                     background='grey',
                     text='').grid(row=(game_pos_y[self.murv[-1][1]] - 1),
                                   column=(game_pos_x[self.murv[-1][0]] - 1))
            self.nombremurv = len(self.murv)

        # Vérifier si un joueur a joué un ou plusieurs de ses murs
        for num, joueur in enumerate(self.joueurs):
            if joueur['murs'] != self.oldjoueurs[num]['murs']:
                tk.Label(self.murholders[num],
                         width=mur_v_dimensions[0],
                         height=mur_v_dimensions[1],
                         padx=5,
                         background='white',
                         text='').grid(column=(joueur['murs'] + 2), row=1)
                self.oldjoueurs[num]['murs'] = joueur['murs']
        if self.playerturn == 1:
            self.playerturn = 2
        elif self.playerturn == 2:
            self.playerturn = 1
        else:
            print("wrong player number")
        self.root.update()
        self.verification_victoire()


    def verification_victoire(self):
        """vérifier si un joueur a gagné. si oui, fenetre popup
        Raises:
            StopIteration: termine le jeu
        """
        t = self.partie_terminée()
        if t:
            mb.showinfo("La partie est terminée!",
                        "le joueur {} à gagné!".format(t))
            self.root.destroy()
            raise StopIteration("partie terminée")


    def bouger_joueur(self, event):
        """handler pour l'event levée l'orsqu'on clique sur une
        case de déplacement de joueur
        Arguments:
            event {event} -- le widget cliqué
        """
        try:
            if self.mode == 'server':
                self.playerturn = 1
            self.déplacer_jeton(self.playerturn,
                                event.widget.extra)
            self.afficher()
            if self.mode == 'server':
                try:
                    nouveaujeu = api.jouer_coup(self.gameid,
                                                'D',
                                                event.widget.extra)
                    self.joueurs = nouveaujeu['joueurs']
                    self.murh = nouveaujeu['murs']['horizontaux']
                    self.murv = nouveaujeu['murs']['verticaux']
                except StopIteration as s:
                    mb.showinfo("La partie est terminée!",
                                "le joueur {} à gagné!".format(s))
                    return
        except (quoridor.QuoridorError,
                nx.exception.NetworkXError,
                nx.exception.NetworkXNoPath) as er:
            mb.showerror("Erreur!", er)
        self.afficher()


    def placer_murh(self, event):
        """Handler pour l'event levée l'orsqu'on clique sur une case
        de placement de mur horizontal
        Arguments:
            event {event} -- le widget cliqué
        """
        try:
            if self.mode == 'server':
                self.playerturn = 1
            self.placer_mur(self.playerturn,
                            event.widget.extra,
                            'horizontal')
            self.afficher()
            if self.mode == 'server':
                try:
                    nouveaujeu = api.jouer_coup(self.gameid,
                                                'MH',
                                                event.widget.extra)
                    self.joueurs = nouveaujeu['joueurs']
                    self.murh = nouveaujeu['murs']['horizontaux']
                    self.murv = nouveaujeu['murs']['verticaux']
                except StopIteration as s:
                    mb.showinfo("La partie est terminée!",
                                "le joueur {} à gagné!".format(s))
                    return
        except (quoridor.QuoridorError,
                nx.exception.NetworkXError,
                nx.exception.NetworkXNoPath) as er:
            mb.showerror("Erreur!", er)
        self.afficher()


    def placer_murv(self, event):
        """Handler pour l'event levée l'orsqu'on clique sur une case
        de placement de mur vertical
        Arguments:
            event {event} -- le widget cliqué
        """
        try:
            if self.mode == 'server':
                self.playerturn = 1
            self.placer_mur(self.playerturn,
                            event.widget.extra,
                            'vertical')
            self.afficher()
            if self.mode == 'server':
                try:
                    nouveaujeu = api.jouer_coup(self.gameid,
                                                'MV',
                                                event.widget.extra)
                    self.joueurs = nouveaujeu['joueurs']
                    self.murh = nouveaujeu['murs']['horizontaux']
                    self.murv = nouveaujeu['murs']['verticaux']
                except StopIteration as s:
                    mb.showinfo("La partie est terminée!",
                                "le joueur {} à gagné!".format(s))
                    return
        except (quoridor.QuoridorError,
                nx.exception.NetworkXError,
                nx.exception.NetworkXNoPath) as er:
            mb.showerror("Erreur!", er)
        self.afficher()


    def hilight(self, event):
        """Handler pour hilighter une case
        l'orsque la sourie passe dessus
        Arguments:
            event {event} -- le widget ciblé
        """
        if self.automode == False:
            event.widget['bg'] = event.widget['activeforeground']


    def unhilight(self, event):
        """Handler pour dé-hilighter une case
        l'orsque la sourie passe dessus
        Arguments:
            event {event} -- le widget ciblé
        """
        if self.automode == False:
            event.widget['bg'] = event.widget['activebackground']




if __name__ == '__main__':
    test = QuoridorX(['joueur1', 'joueur2'])
    tk.mainloop()
