"""quoridor.py
Module pour contenir la classe QuoridorX
"""
import tkinter as tk
import copy
import itertools
import quoridor


def hilight(event):
    """Handler pour hilighter une case
    l'orsque la sourie passe dessus
    Arguments:
        event {event} -- le widget ciblé
    """
    event.widget['bg'] = event.widget['activeforeground']
def unhilight(event):
    """Handler pour dé-hilighter une case
    l'orsque la sourie passe dessus
    Arguments:
        event {event} -- le widget ciblé
    """
    event.widget['bg'] = event.widget['activebackground']


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
        self.task = []
        # lists of equivalent positions
        game_pos_x = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]
        game_pos_y = [0, 17, 15, 13, 11, 9, 7, 5, 3, 1]
        game_pos_mur = [0, 2, 4, 6, 8, 10, 12, 14, 16]
        # Créer la table de jeu
        self.make_board()
        # dresser la table de jeu
        for i, j in itertools.product(range(1, 18), range(1, 18)):
            # Cases de jeu principales
            for numero, joueur in enumerate(self.joueurs):
                # Si un joueur est sur cette case
                if (game_pos_x[joueur['pos'][0]], game_pos_y[joueur['pos'][1]]) == (i, j):
                    self.make_cases(i, j, 'blue', '#ffcc99', t=str(numero + 1))
                    break
                else:
                    # Sinon, faire une case de jeu normale
                    if (i in game_pos_x) and (j in game_pos_y):
                        self.make_cases(i, j, 'blue', '#f9f9eb',
                                        extr=(game_pos_x.index(i),
                                              game_pos_y.index(j)))
            # Murs horizontaux
            if len(self.murh) > 0:
                for wallh in self.murh:
                    if (game_pos_x[wallh[0]], game_pos_y[wallh[1]]) == (i, (j - 1)):
                        self.make_murh(i, j, 'blue', 'grey')
                        # remplissage de la case vide
                        tk.Label(self.board,
                                 width=1,
                                 height=1,
                                 borderwidth=1,
                                 relief=tk.FLAT,
                                 takefocus=True,
                                 highlightcolor='blue',
                                 highlightthickness=5,
                                 background='grey',
                                 text='').grid(row=j, column=(i + 1))
                        break
                    # décallage: x + 1
                    elif (game_pos_x[(wallh[0] + 1)], game_pos_y[wallh[1]]) == (i, (j - 1)):
                        self.make_murh(i, j, 'blue', 'grey')
                        break
                    else:
                        if (i in game_pos_x) and (j in game_pos_mur):
                            self.make_murh(i, j, 'blue', 'brown',
                                           (game_pos_x.index(i),
                                            game_pos_y.index(j - 1)))
            else:
                if (i in game_pos_x) and (j in game_pos_mur):
                    self.make_murh(i, j, 'blue', 'brown',
                                   (game_pos_x.index(i), game_pos_y.index(j - 1)))
            #Murs verticaux
            if len(self.murv) > 0:
                for wallv in self.murv:
                    if (game_pos_x[wallv[0]], game_pos_y[wallv[1]]) == ((i + 1), j):
                        self.make_murv(i, j, 'blue', 'grey')
                        # remplissage de la case vide
                        tk.Label(self.board,
                                 width=1,
                                 height=1,
                                 borderwidth=1,
                                 relief=tk.FLAT,
                                 takefocus=True,
                                 highlightcolor='blue',
                                 highlightthickness=5,
                                 background='grey',
                                 text='').grid(row=(j - 1), column=i)
                        break
                    # décallage: y + 1
                    elif (game_pos_x[wallv[0]], game_pos_y[(wallv[1] + 1)]) == ((i + 1), j):
                        self.make_murv(i, j, 'blue', 'grey')
                        break
                    else:
                        if (i in game_pos_mur) and (j in game_pos_y):
                            self.make_murv(i, j, 'blue', 'brown',
                                           (game_pos_x.index(i + 1),
                                            game_pos_y.index(j)))
            else:
                if (i in game_pos_mur) and (j in game_pos_y):
                    self.make_murv(i, j, 'blue', 'brown',
                                   (game_pos_x.index(i + 1), game_pos_y.index(j)))

    def afficher(self):
        """met à jours l'affichage
        """
        # lists of equivalent positions
        game_pos_x = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]
        game_pos_y = [0, 17, 15, 13, 11, 9, 7, 5, 3, 1]
        # vérifier si le joueur a bougé
        for i in range(2):
            if self.oldjoueurs[i]['pos'] != self.joueurs[i]['pos']:
                #effacer l'ancienne position du joueur
                self.make_cases(game_pos_x[self.oldjoueurs[i]['pos'][0]],
                                game_pos_y[self.oldjoueurs[i]['pos'][1]],
                                'blue', '#f9f9eb', extr=self.oldjoueurs[i]['pos'])
                self.oldjoueurs[i]['pos'] = self.joueurs[i]['pos']
                # Afficher la nouvelle case du joueur
                self.make_cases(game_pos_x[self.oldjoueurs[i]['pos'][0]],
                                game_pos_y[self.oldjoueurs[i]['pos'][1]],
                                'blue',
                                '#ffcc99',
                                t=str(i + 1),
                                extr=self.oldjoueurs[i]['pos'])

        # Vérifier si des murs horizontaux ont été placés
        if self.nombremurh < len(self.murh):
            for i in range(2):
                self.make_murh((game_pos_x[self.murh[-1][0]] + (2 * i)),
                               (game_pos_y[self.murh[-1][1]] + 1),
                               'blue', 'grey')
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
                self.make_murv((game_pos_x[self.murv[-1][0]] - 1),
                               (game_pos_y[self.murv[-1][1]] - (2 * i)),
                               'blue', 'grey')
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
                     text='').grid(row=(game_pos_y[self.murv[-1][1]] - 1),
                                   column=(game_pos_x[self.murv[-1][0]] - 1))
            self.nombremurv = len(self.murv)

        # Vérifier si un joueur a joué un ou plusieurs de ses murs
        for num, joueur in enumerate(self.joueurs):
            if joueur['murs'] != self.oldjoueurs[num]['murs']:
                tk.Label(self.murholders[num],
                         width=1,
                         height=3,
                         padx=5,
                         background='white',
                         text='').grid(column=(joueur['murs'] + 2), row=1)
                self.oldjoueurs[num]['murs'] = joueur['murs']
        self.root.update()

    def make_board(self):
        """Handler pour construire le tableau autour du jeu
        """
        # Make row labels
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
                         width=1,
                         height=3,
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
    
    def make_cases(self, i, j, fr, ba, t='', extr=None):
        """Handler pour créer les cases principales du jeu
        Arguments:
            i {int} -- numéro de colonne du widget
            j {int} -- numéro de rangée du widget
            fr {str} -- couleur de hilight
            ba {str} -- couleur de background
        Keyword Arguments:
            t {str} -- text à afficher (default: {''})
            extr {tuple} -- extra en cas de logique a attacher (default: {None})
        """
        lab = tk.Label(self.board,
                       width=3,
                       height=3,
                       relief=tk.FLAT,
                       borderwidth=1,
                       background=ba,
                       activeforeground=fr,
                       activebackground=ba,
                       highlightthickness=5,
                       text=t)
        lab.grid(row=j, column=i)
        if extr:
            lab.extra = extr
            lab.bind("<Button-1>", self.bouger_joueur)
            lab.bind("<Enter>", hilight)
            lab.bind("<Leave>", unhilight)

    def make_murh(self, i, j, fr, ba, extr=None):
        """Handler pour créer les cases principales du jeu
        Arguments:
            i {int} -- numéro de colonne du widget
            j {int} -- numéro de rangée du widget
            fr {str} -- couleur de hilight
            ba {str} -- couleur de background
        Keyword Arguments:
            extr {tuple} -- extra en cas de logique a attacher (default: {None})
        """
        lab = tk.Label(self.board,
                       width=3,
                       height=1,
                       relief=tk.FLAT,
                       borderwidth=1,
                       background=ba,
                       activeforeground=fr,
                       activebackground=ba,
                       highlightthickness=5
                      )
        lab.grid(row=j, column=i)
        if extr:
            lab.extra = extr
            lab.bind("<Button-1>", self.placer_murh)
            lab.bind("<Enter>", hilight)
            lab.bind("<Leave>", unhilight)

    def make_murv(self, i, j, fr, ba, extr=None):
        """Handler pour créer les cases principales du jeu
        Arguments:
            i {int} -- numéro de colonne du widget
            j {int} -- numéro de rangée du widget
            fr {str} -- couleur de hilight
            ba {str} -- couleur de background
        Keyword Arguments:
            extr {tuple} -- extra en cas de logique a attacher (default: {None})
        """
        lab = tk.Label(self.board,
                       width=1,
                       height=3,
                       relief=tk.FLAT,
                       borderwidth=1,
                       background=ba,
                       activeforeground=fr,
                       activebackground=ba,
                       highlightthickness=5
                      )
        lab.grid(row=j, column=i)
        if extr:
            lab.extra = extr
            lab.bind("<Button-1>", self.placer_murv)
            lab.bind("<Enter>", hilight)
            lab.bind("<Leave>", unhilight)

    def bouger_joueur(self, event):
        """handler pour l'event levée l'orsqu'on clique sur une
        case de déplacement de joueur
        Arguments:
            event {event} -- le widget cliqué
        """
        self.task = ['D',
                     event.widget.extra[0],
                     event.widget.extra[1]]

    def placer_murh(self, event):
        """Handler pour l'event levée l'orsqu'on clique sur une case
        de placement de mur horizontal
        Arguments:
            event {event} -- le widget cliqué
        """
        self.task = ['MH',
                     event.widget.extra[0],
                     event.widget.extra[1]]

    def placer_murv(self, event):
        """Handler pour l'event levée l'orsqu'on clique sur une case
        de placement de mur vertical
        Arguments:
            event {event} -- le widget cliqué
        """
        self.task = ['MV',
                     event.widget.extra[0],
                     event.widget.extra[1]]


if __name__ == '__main__':
    QO = QuoridorX(['joueur1', 'joueur2'])
    tk.mainloop()
