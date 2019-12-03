"""quoridor.py
Module pour contenir la classe QuoridorX
"""
import quoridor
import tkinter as tk
import turtle as tl



class QuoridorX(quoridor.Quoridor):

    def afficher(self):
        """draws a 9x9 grid
        """
        root = tk.Tk()
        # lists of equivalent positions
        game_pos_x = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17]
        game_pos_y = [0, 17, 15, 13, 11, 9, 7, 5, 3, 1]
        game_pos_mur = [0, 2, 4, 6, 8, 10, 12, 14, 16]

        """tailles du tableau:
        largeur: 17 char
        heuteur: 17 lignes
        """
        # sizes of the different labels [height, width]
        case_jeu_dimensions = [3, 3]
        mur_h_dimensions = [3, 1]
        mur_v_dimensions = [1, 3]
        # filling the things
        # make row labels
        for r in range(1, 18):
            if (r % 2) == 0:
                tk.Label(root,
                         text=str(10-(((r + 1) // 2) + 1))).grid(row=(r+1), column=1)
        #board = tk.Frame(root, background='brown' ,borderwidth=10 ,padx=10, pady=10, relief=tk.RIDGE)
        board = tk.Frame(root, background='brown' ,borderwidth=10 , relief=tk.RIDGE)
        board.grid(column=2,
                    columnspan=17,
                    padx=50,
                    pady=50,
                    row=2,
                    rowspan=17,
                    sticky='n')

        # ajouter le contour du tableau

        # dresser la table de jeu
        for i in range(1, 18):
            for j in range(1, 18):
                
                # Cases de jeu principales
                for numero, joueur in enumerate(self.joueurs):
                    if (game_pos_x[joueur['pos'][0]], game_pos_y[joueur['pos'][1]]) == (i, j):
                        case = tk.Frame(board,
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
                            case = tk.Frame(board,
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
                            case = tk.Frame(board,
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
                            case = tk.Frame(board,
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
                            case = tk.Frame(board,
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
                                case = tk.Frame(board,
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
                        case = tk.Frame(board,
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
                            case = tk.Frame(board,
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
                            case = tk.Frame(board,
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
                            case = tk.Frame(board,
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
                                case = tk.Frame(board,
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
                        case = tk.Frame(board,
                                        background='brown',
                                        borderwidth=1,
                                        relief=tk.FLAT)  
                        case.grid(row=j, column =i)
                        tk.Label(case,
                                 width = mur_v_dimensions[0],
                                 height=mur_v_dimensions[1],
                                 background='brown',
                                 text='').grid(row=j, column =i)
                        


        root.mainloop()




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
    test.afficher()