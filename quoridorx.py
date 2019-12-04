"""quoridor.py
Module pour contenir la classe QuoridorX
"""
import quoridor
import tkinter as tk
import copy



class QuoridorX(quoridor.Quoridor):


    def __init__(self, joueurs, murs=None):
        """initialisation de l'affichage du jeu
        
        Arguments:
            joueurs {[type]} -- [description]
        
        Keyword Arguments:
            murs {[type]} -- [description] (default: {None})
        TODO: ajouter une visualisation des murs que chaque joueurs peuvent encore placer
        TODO: améliorer le look de absolument tout
        TODO: rendre toutes les grandeurs scalables avec les fenêtres
        """
        super().__init__(joueurs, murs)

        self.root = tk.Tk()
        #self.posjoueurs = [self.joueurs[0]['pos'], self.joueurs[1]['pos']]
        self.oldjoueurs = copy.deepcopy(self.joueurs)
        self.nombremurh = len(self.murh)
        self.nombremurv = len(self.murv)
        self.murholders = [0, 0]
        
        # lists of equivalent positions
        game_pos_x = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]
        game_pos_y = [0, 17, 15, 13, 11, 9, 7, 5, 3, 1]
        game_pos_mur = [0, 2, 4, 6, 8, 10, 12, 14, 16]
        # sizes of the different labels [height, width]
        case_jeu_dimensions = [3, 3]
        mur_h_dimensions = [3, 1]
        mur_v_dimensions = [1, 3]
        # Make Header
        tk.Label(self.root,
                 width=17,
                 height=1,
                 text="Légende: 1={} 2={}".format(self.joueurs[0]['nom'], self.joueurs[1]['nom'])
                 ).grid(row=1, column=2)
        
        # make row labels
        self.row_label_frame = tk.Frame(self.root, background='brown' ,borderwidth=2 , relief=tk.RIDGE)
        self.row_label_frame.grid(column=1,
                                  columnspan=1,
                                  row=4,
                                  rowspan=17,
                                  sticky='n')
        for r in range(1, 18):
            if (r % 2) != 0:
                case = tk.Frame(self.row_label_frame,
                                background='blue',
                                borderwidth=1,
                                relief=tk.FLAT)
                case.grid(row = r, column = 1)
                tk.Label(case,
                         width = 1,
                         height=3,
                         text=str(10-(((r + 1) // 2)))).grid(row=(r), column=1)
            else:
                case = tk.Frame(self.row_label_frame,
                                background='blue',
                                borderwidth=1,
                                relief=tk.FLAT)
                case.grid(row =r, column=1)
                tk.Label(case,
                         width = 1,
                         height=1,
                         text="").grid(row=(r), column=1)
        
        # Make column labels
        self.column_label_frame = tk.Frame(self.root, background='brown' ,borderwidth=2 , relief=tk.RIDGE)
        self.column_label_frame.grid(column=2,
                                     columnspan=17,
                                     row=21,
                                     rowspan=1,
                                     sticky='n')
        for c in range(1, 18):
            if (c % 2) != 0:
                case = tk.Frame(self.column_label_frame,
                                background='blue',
                                borderwidth=1,
                                relief=tk.FLAT)
                case.grid(row = 1, column = c)
                tk.Label(case,
                         width = 3,
                         height=1,
                         text=str((((c + 1) // 2)))).grid(row=1, column=c)
            else:
                case = tk.Frame(self.column_label_frame,
                                background='blue',
                                borderwidth=1,
                                relief=tk.FLAT)
                case.grid(row =1, column=c)
                tk.Label(case,
                         width = 1,
                         height=1,
                         text="").grid(row=1, column=c)

        # Afficher les murs que chaque joueurs peuvent encore placer
        for num, r in enumerate([24, 3]):
            # Murs des 2 joueurs
            tk.Label(self.root,
                     text="Joueur {} = {}".format((num + 1), self.joueurs[num]['nom']),
                     height=1).grid(column=3,row=(r - 1))
            self.murholders[num] = tk.Frame(self.root,
                                    background='grey',
                                    borderwidth=2,
                                    relief=tk.FLAT)
            self.murholders[num].grid(column=2,
                                      columnspan=17,
                                      row=r,
                                      rowspan=1,
                                      sticky='n')
            #tk.Label(self.murholders[num],
            #         text="Joueur {}".format((num + 1))).grid(row=1, column=1)
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
        self.board = tk.Frame(self.root, background='brown' ,borderwidth=2 , relief=tk.RIDGE)
        self.board.grid(column=2,
                        columnspan=17,
                        row=4,
                        rowspan=17,
                        sticky='n')

        # dresser la table de jeu
        for i in range(1, 18):
            for j in range(1, 18):
                
                # Cases de jeu principales
                for numero, joueur in enumerate(self.joueurs):
                    if (game_pos_x[joueur['pos'][0]], game_pos_y[joueur['pos'][1]]) == (i, j):
                        case = tk.Frame(self.board,
                                        background='blue',
                                        borderwidth=1,
                                        relief=tk.FLAT)
                        case.grid(row=j, column =i)
                        tk.Label(case,
                                 width = case_jeu_dimensions[0],
                                 height=case_jeu_dimensions[1],
                                 background='#ffcc99',
                                 text=str(numero + 1)).grid(row=j, column =i)
                        break
                    else:
                        if (i in game_pos_x) and (j in game_pos_y):
                            case = tk.Frame(self.board,
                                            background='blue',
                                            borderwidth=1,
                                            relief=tk.FLAT)  
                            case.grid(row=j, column =i)
                            tk.Label(case,
                                    width = case_jeu_dimensions[0],
                                    height=case_jeu_dimensions[1],
                                    background='#bfbfbf',
                                    text='').grid(row=j, column =i)
                
                # Murs horizontaux
                if len(self.murh) > 0:
                    for wallh in self.murh:
                        if (game_pos_x[wallh[0]], game_pos_y[wallh[1]]) == (i, (j - 1)):
                            case = tk.Frame(self.board,
                                            background='grey',
                                            borderwidth=1,
                                            relief=tk.FLAT)  
                            case.grid(row=j, column =i)
                            tk.Label(case,
                                    width = mur_h_dimensions[0],
                                    height=mur_h_dimensions[1],
                                    background='grey',
                                    text='').grid(row=j, column =i)
                            # remplissage de la case vide
                            case = tk.Frame(self.board,
                                            background='grey',
                                            borderwidth=1,
                                            relief=tk.FLAT)  
                            case.grid(row=j, column =(i + 1))
                            tk.Label(case,
                                    width = 1,
                                    height=1,
                                    background='grey',
                                    text='').grid(row=j, column =(i + 1))
                            break
                        # décallage: x + 1
                        elif (game_pos_x[(wallh[0] + 1)], game_pos_y[wallh[1]]) == (i, (j - 1)):
                            case = tk.Frame(self.board,
                                            background='grey',
                                            borderwidth=1,
                                            relief=tk.FLAT)  
                            case.grid(row=j, column =i)
                            tk.Label(case,
                                    width = mur_h_dimensions[0],
                                    height=mur_h_dimensions[1],
                                    background='grey',
                                    text='').grid(row=j, column =i)
                            break
                        else:
                            if (i in game_pos_x) and (j in game_pos_mur):
                                case = tk.Frame(self.board,
                                                background='brown',
                                                borderwidth=1,
                                                relief=tk.FLAT)  
                                case.grid(row=j, column =i)
                                tk.Label(case,
                                        width = mur_h_dimensions[0],
                                        height=mur_h_dimensions[1],
                                        background='brown',
                                        text='').grid(row=j, column =i)
                else:
                    if (i in game_pos_x) and (j in game_pos_mur):
                        case = tk.Frame(self.board,
                                        background='brown',
                                        borderwidth=1,
                                        relief=tk.FLAT)  
                        case.grid(row=j, column =i)
                        tk.Label(case,
                                 width = mur_h_dimensions[0],
                                 height=mur_h_dimensions[1],
                                 background='brown',
                                 text='').grid(row=j, column =i)
                
                #Murs verticaux
                if len(self.murv) > 0:
                    for wallv in self.murv:
                        if (game_pos_x[wallv[0]], game_pos_y[wallv[1]]) == ((i + 1), j):
                            case = tk.Frame(self.board,
                                            background='grey',
                                            borderwidth=1,
                                            relief=tk.FLAT)
                            case.grid(row=j, column =i)
                            tk.Label(case,
                                    width = mur_v_dimensions[0],
                                    height=mur_v_dimensions[1],
                                    background='grey',
                                    text='').grid(row=j, column =i)
                            # remplissage de la case vide
                            case = tk.Frame(self.board,
                                            background='grey',
                                            borderwidth=1,
                                            relief=tk.FLAT)
                            case.grid(row=(j - 1), column =i)
                            tk.Label(case,
                                    width = 1,
                                    height=1,
                                    background='grey',
                                    text='').grid(row=(j - 1), column =i)
                            break
                        # décallage: y + 1
                        elif (game_pos_x[wallv[0]], game_pos_y[(wallv[1] + 1)]) == ((i + 1), j):
                            case = tk.Frame(self.board,
                                            background='grey',
                                            borderwidth=1,
                                            relief=tk.FLAT)  
                            case.grid(row=j, column =i)
                            tk.Label(case,
                                    width = mur_v_dimensions[0],
                                    height=mur_v_dimensions[1],
                                    background='grey',
                                    text='').grid(row=j, column =i)
                            break
                        else:
                            if (i in game_pos_mur) and (j in game_pos_y):
                                case = tk.Frame(self.board,
                                                background='brown',
                                                borderwidth=1,
                                                relief=tk.FLAT)
                                case.grid(row=j, column =i)
                                tk.Label(case,
                                        width = mur_v_dimensions[0],
                                        height=mur_v_dimensions[1],
                                        background='brown',
                                        text=' ').grid(row=j, column =i)
                else:
                    if (i in game_pos_mur) and (j in game_pos_y):
                        case = tk.Frame(self.board,
                                        background='brown',
                                        borderwidth=1,
                                        relief=tk.FLAT)  
                        case.grid(row=j, column =i)
                        tk.Label(case,
                                 width = mur_v_dimensions[0],
                                 height=mur_v_dimensions[1],
                                 background='brown',
                                 text='').grid(row=j, column =i)

 
    def afficher(self):
        """met à jours l'affichage
        """
        print("affichage")
        # lists of equivalent positions
        game_pos_x = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]
        game_pos_y = [0, 17, 15, 13, 11, 9, 7, 5, 3, 1]
        # sizes of the different labels [height, width]
        case_jeu_dimensions = [3, 3]
        mur_h_dimensions = [3, 1]
        mur_v_dimensions = [1, 3]
        # vérifier si le joueur a bougé
        for i in range(2):
            print(self.oldjoueurs[i]['pos'])
            print(self.joueurs[i]['pos'])
            if self.oldjoueurs[i]['pos'] != self.joueurs[i]['pos']:
                #effacer l'ancienne position du joueur
                oldcase = tk.Frame(self.board,
                                background='blue',
                                borderwidth=1,
                                relief=tk.FLAT)
                oldcase.grid(row=game_pos_y[self.oldjoueurs[i]['pos'][1]],
                             column=game_pos_x[self.oldjoueurs[i]['pos'][0]])
                tk.Label(oldcase,
                         width = case_jeu_dimensions[0],
                         height=case_jeu_dimensions[1],
                         background='#bfbfbf',
                         text='').grid(row=game_pos_y[self.oldjoueurs[i]['pos'][1]],
                                       column=game_pos_x[self.oldjoueurs[i]['pos'][0]])
                
                self.oldjoueurs[i]['pos'] = self.joueurs[i]['pos']
                
                newcase = tk.Frame(self.board,
                                   background='blue',
                                   borderwidth=1,
                                   relief=tk.FLAT)
                newcase.grid(row=game_pos_y[self.oldjoueurs[i]['pos'][1]],
                             column=game_pos_x[self.oldjoueurs[i]['pos'][0]])
                tk.Label(newcase,
                         width=case_jeu_dimensions[0],
                         height=case_jeu_dimensions[1],
                         background='#ffcc99',
                         text=str(i + 1)).grid(row=game_pos_y[self.oldjoueurs[i]['pos'][1]],
                                               column=game_pos_x[self.oldjoueurs[i]['pos'][0]])
        
        # Vérifier si des murs horizontaux ont été placés
        if self.nombremurh < len(self.murh):
            for i in range(2):
                case = tk.Frame(self.board,
                                background='grey',
                                borderwidth=1,
                                relief=tk.FLAT)
                case.grid(row=(game_pos_y[self.murh[-1][1]] + 1),
                          column=(game_pos_x[self.murh[-1][0]] + (2 * i)))
                tk.Label(case,
                        width=mur_h_dimensions[0],
                        height=mur_h_dimensions[1],
                        background='grey',
                        text='').grid(row=(game_pos_y[self.murh[-1][1]] + 1),
                                      column=(game_pos_x[self.murh[-1][0]] + (2 * i)))
            # Remplissage de la case vide
            case = tk.Frame(self.board,
                            background='grey',
                            borderwidth=1,
                            relief=tk.FLAT)  
            case.grid(row=(game_pos_y[self.murh[-1][1]] + 1),
                      column=(game_pos_x[self.murh[-1][0]] + 1))
            tk.Label(case,
                     width = 1,
                     height=1,
                     background='grey',
                     text='').grid(row=(game_pos_y[self.murh[-1][1]] + 1),
                                   column=(game_pos_x[self.murh[-1][0]] + 1))
            self.nombremurh = len(self.murh)
        
        # Vérifier si des murs verticaux ont été placés
        if self.nombremurv < len(self.murv):
            for i in range(2):
                case = tk.Frame(self.board,
                                background='grey',
                                borderwidth=1,
                                relief=tk.FLAT)
                case.grid(row=(game_pos_y[self.murv[-1][1]] - (2 * i)),
                          column=(game_pos_x[self.murv[-1][0]] - 1))
                tk.Label(case,
                        width=mur_v_dimensions[0],
                        height=mur_v_dimensions[1],
                        background='grey',
                        text='').grid(row=(game_pos_y[self.murv[-1][1]] - (2 * i)),
                                      column=(game_pos_x[self.murv[-1][0]] - 1))
            # Remplissage de la case vide
            case = tk.Frame(self.board,
                            background='grey',
                            borderwidth=1,
                            relief=tk.FLAT)  
            case.grid(row=(game_pos_y[self.murv[-1][1]] - 1),
                           column=(game_pos_x[self.murv[-1][0]] - 1))
            tk.Label(case,
                     width = 1,
                     height=1,
                     background='grey',
                     text='').grid(row=(game_pos_y[self.murv[-1][1]] - 1),
                                   column=(game_pos_x[self.murv[-1][0]] - 1))
            self.nombremurv = len(self.murv)

        # Vérifier si un joueur a joué un ou plusieurs de ses murs
        for num, joueur in enumerate(self.joueurs):
            if joueur['murs'] != self.oldjoueurs[num]['murs']:
                cadre = tk.Frame(self.murholders[num],
                                 background='grey',
                                 borderwidth=3,
                                 padx=5,
                                 relief=tk.RIDGE)
                cadre.grid(column=(joueur['murs'] + 1), row=1)
                tk.Label(cadre,
                         width=mur_v_dimensions[0],
                         height=mur_v_dimensions[1],
                         padx=5,
                         background='white',
                         text='').grid(column=(joueur['murs'] + 1), row=1)
                
                self.oldjoueurs[num]['murs'] = joueur['murs']


        self.root.update()




if __name__ == '__main__':
    partie_existante_etat = {
            "joueurs": [
                {"nom": "foo", "murs": 7, "pos": [5, 6]},
                {"nom": "bar", "murs": 3, "pos": [5, 7]}
            ],
            "murs": {
                "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
            }}
    #test = QuoridorX(["player1", "player2"])
    test = QuoridorX(partie_existante_etat['joueurs'], partie_existante_etat['murs'])
    tk.mainloop()
    #test.afficher()