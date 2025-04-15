from fileinput import filename
from pprint import pprint
import sys
from typing import List
import copy

def complete(m: List[List[str]], n: int):
    for l in m:
        for _ in range(len(l), n):
            l.append(" ")
    return m


def grid_from_file(filename: str):

    grid = []
    m = 0  # nombre de lignes
    n = 0  # nombre de colonnes
    no = 0  # numéro de ligne du fichier
    title = ""
    max_steps = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            no += 1

            l = line.rstrip()

            if no == 1:
                title = l
                continue
            if no == 2:
                max_steps = int(l)
                continue

            if len(l) > n:
                n = len(l)
                complete(grid, n)

            if l != "":
                grid.append(list(l))

    m = len(grid)

    return {"grid": grid, "title": title, "m": m, "n": n, "max_steps": max_steps}


dicoinit={ #dico des fluents
    "#": "M",
    "H": "R",
    "D": "F",
    " ": " ",
    "B": "C",
    "K": " ",
    "L": "T",
    "M": "Z",
    "S": " ",
    "T": " ",
    "U": " ",
    "O": "C",
    "P": "C",
    "Q": "C",
}

dicoimm={   #dico de termes immobiles
    "#": " ",
    "H": " ",
    "D": " ",
    " ": " ",
    "B": " ",
    "K": "K",
    "L": " ",
    "M": " ",
    "S": "D",
    "T": "I",
    "U": "P",
    "O": "D",
    "P": "I",
    "Q": "P",
}
def remplissage_grilles(dicoinit,dicoimm,grille):
    init=[]
    imm=[]
    for x in range(len(grille)):
        initint=[]
        immint=[]
        for y in range(len(grille[x])):
            initint.append(dicoinit[grille[x][y]])
            immint.append(dicoimm[grille[x][y]])
        init.append(initint)
        imm.append(immint)
    return init, imm


def haut(x,y,t):
    return t[x-1][y]
def bas(x,y,t):
    return t[x+1][y]
def droit(x,y,t):
    return t[x][y+1]
def gauche(x,y,t):
    return t[x][y-1]


def h(x,y,t,imm,gagne, croc, cle):
#premier cas à prendre en compte dans tous les cas si un zombie se trouve sur des crocs ou le perso ou la clé
    if (x<=0 or y<0 or y>=len(t[0]) or x>=len(t)):
        return (t,gagne,croc,cle)
        
    for a in range (0,len(t)):
        for b in range (0,len(t[a])):
            if t[a][b] == "Z":
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0):
                    t[a][b] = " "
            if t[a][b] == "R":
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0):
                    gagne-=1
                if imm[a][b] == "K":
                    cle = True
                    

    if (haut(x,y,t) == "Z"):
        if(haut(x-1,y,t) == "C") or (haut(x-1,y,t) == "M") or (haut(x-1,y,t) == "T") or (haut(x-1,y,t) == "Z") or (haut(x-1,y,t) == "F"):
            t[x-1][y] = " "
        elif (x-2>=0):
            t[x-2][y] = "Z"
            t[x-1][y] = " "
    elif (haut(x,y,t) == "C"):
        if(haut(x-1,y,t) == " " and (x-2>=0)):
            t[x-2][y] = "C"
            t[x-1][y] = " "
    elif(haut(x,y,t) == " "):
        t[x-1][y] = "R"
        t[x][y] = " "
    elif(haut(x,y,t) == "M"):
        return (t,gagne,croc,cle)
    elif(haut(x,y,t) == "T"):
        if cle == True:
            t[x-1][y] = "R"
            t[x][y] = " "
    
    croc+=1
    gagne-=1
    return (t,gagne,croc,cle)

def b(x,y,t,imm,gagne,croc,cle):
    #premier cas à prendre en compte dans tous les cas si un zombie se trouve sur des crocs ou le perso ou la clé
    if (x+1>=len(t)or y<0 or y>=len(t[0]) or x<0):
        return (t,gagne,croc,cle)
        
    for a in range (0,len(t)):
        for b in range (0,len(t[a])):
            if t[a][b] == "Z": 
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0): 
                    t[a][b] = " "
            if t[a][b] == "R":
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0): 
                    gagne-=1
                if imm[a][b] == "K":
                    cle = True
                    
         
    if(bas(x,y,t) == "Z"):
        if(bas(x+1,y,t) == "C") or (bas(x+1,y,t) == "M") or (bas(x+1,y,t) == "T") or (bas(x+1,y,t) == "Z") or (bas(x+1,y,t) == "F"):
            t[x+1][y] = " "
        elif (x+2<len(t)):
            t[x+2][y] = "Z"
            t[x+1][y] = " "
    elif (bas(x,y,t) == "C"):
        if(bas(x+1,y,t) == " " and (x+2<len(t))):
            t[x+2][y] = "C"
            t[x+1][y] = " "
    elif(bas(x,y,t) == " "):
        t[x+1][y] = "R"
        t[x][y] = " "
    elif(bas(x,y,t) == "M"):
        return (t,gagne,croc,cle)
    elif(bas(x,y,t) == "T"):
        if cle == True:
            t[x+1][y] = "R"
            t[x][y] = " "
    croc+=1
    gagne-=1
    return (t,gagne,croc,cle)

def d(x,y,t,imm,gagne,croc,cle):
    #premier cas à prendre en compte dans tous les cas si un zombie se trouve sur des crocs ou le perso ou la clé
    if (y+1>=len(t[0]) or x<0 or x>=len(t) or y<0):
        return (t,gagne,croc,cle)
        
    for a in range (0,len(t)):
        for b in range (0,len(t[a])):
            if t[a][b] == "Z": 
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0): 
                    t[a][b] = " "
            if t[a][b] == "R":
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0): 
                    gagne-=1
                if imm[a][b] == "K":
                    cle = True

    #print(f"x : {x}, y : {y}")
    if(droit(x,y,t) == "Z"):
        if(droit(x,y+1,t) == "C") or (droit(x,y+1,t) == "M") or (droit(x,y+1,t) == "T") or (droit(x,y+1,t) == "Z") or (droit(x,y+1,t) == "F"):
            t[x][y+1] = " "
        elif (y+2<len(t[0])):
            t[x][y+2] = "Z"
            t[x][y+1] = " "
    elif (droit(x,y,t) == "C"):
        if(droit(x,y+1,t) == " " and (y+2<len(t[0]))):
            t[x][y+2] = "C"
            t[x][y+1] = " "
    elif(droit(x,y,t) == " "):
        t[x][y+1] = "R"
        t[x][y] = " "
    elif(droit(x,y,t) == "M"):
        return (t,gagne,croc,cle)
    elif(droit(x,y,t) == "T"):
        if cle == True:
            t[x][y+1] = "R"
            t[x][y] = " "
    croc+=1
    gagne-=1
    return (t,gagne,croc,cle)

def g(x,y,t,imm,gagne,croc,cle):
    #premier cas à prendre en compte dans tous les cas si un zombie se trouve sur des crocs ou le perso ou la clé
    if (y<=0 or x<0 or x>=len(t) or y>=len(t[0])):
        return (t,gagne,croc,cle)
        
    for a in range (0,len(t)):
        for b in range (0,len(t[a])):
            if t[a][b] == "Z": 
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0): 
                    t[a][b] = " "
            if t[a][b] == "R":
                if (imm[a][b] == "P" and croc%2 == 0) or (imm[a][b] == "I" and croc%2 != 0): 
                    gagne-=1
                if imm[a][b] == "K":
                    cle = True

                
    if(gauche(x,y,t) == "Z"):
        if(gauche(x,y-1,t) == "C") or (gauche(x,y-1,t) == "M") or (gauche(x,y-1,t) == "T") or (gauche(x,y-1,t) == "Z") or (gauche(x,y-1,t) == "F"):
            t[x][y-1] = " "
        elif (y-2>=0):
            t[x][y-2] = "Z"
            t[x][y-1] = " "
    elif (gauche(x,y,t) == "C"):
        if(gauche(x,y-1,t) == " " and (y-2>=0)):
            t[x][y-2] = "C"
            t[x][y-1] = " "
    elif(gauche(x,y,t) == " "):
        t[x][y-1] = "R"
        t[x][y] = " "
    elif(gauche(x,y,t) == "M"):
        return (t,gagne,croc,cle)
    elif(gauche(x,y,t) == "T"):
        if cle == True:
            t[x][y-1] = "R"
            t[x][y] = " "
    croc+=1
    gagne-=1
    return (t,gagne,croc,cle)


def verif(t):
    for a in range (0,len(t)):
        for b in range (0,len(t[a])):
            if t[a][b] == "R" and (t[a-1][b] == "F" or t[a+1][b] == "F" or t[a][b-1] == "F" or t[a][b+1] == "F"):
                return True
    return False

def verif_plan(la,t,imm,gagne,croc,cle):
    for i in range (0,len(la)):
        for a in range (0,len(t)):
            for k in range (0,len(t[a])):
                if t[a][k] == "R":
                    x=a
                    y=k
        
        t,gagne,croc,cle=eval(la[i])(x,y,t,imm,gagne,croc,cle)
        #affiche(t)
        if gagne<0:
            return False
    if verif(t) == True:
        return True
    else:
        return False	

def affiche(t):
    for i in range(len(t)):
        print("\n")
        for j in range(len(t[i])):
            if (t[i][j] == "M"):
                print("* ", end='')
            else:
                print(t[i][j]+" ", end='')
    print('\n________________________')



def findTarget(imm, key):
    keys = []
    for i in range(len(imm)):
        for j in range(len(imm[i])):
            if(imm[i][j] == key):
                keys.append(str(i)+str(j))
    return keys


# poids 2 :  
# a cote d'un zombie qui peut etre poussé, on reste sur la case et le poids s'incrémente    
def dico_voisins_satisfiables(liste,imm,gagne, croc, cle): #Algo qui répertorie tous les voisins de chaque case dans un dictionnaire à partir d'une liste qui représente l'état du jeu
    #Les lettres correspondent aux lignes de la matrice et les chiffres de 1 à n correspondent aux colonnes de la matrice
    #la liste est une matrice, donc une liste de liste
    dic={}
    v=0

    for i in range(len(liste)):
        for j in range(len(liste[0])):
            liste_init = copy.deepcopy(liste)
            interm=[]
            conc=str(i)+str(j)
            (t1,hl,croc1,cle1)=h(i,j,liste_init,imm,gagne, croc, cle)
            liste_init = copy.deepcopy(liste)
            dhl = gagne - hl+croc1
            (t2,dl,croc2,cle2)=d(i,j,liste_init,imm,gagne, croc, cle)
            liste_init = copy.deepcopy(liste)
            ddl = gagne - dl +croc2
            (t3,bl,croc3,cle3)=b(i,j,liste_init,imm,gagne, croc, cle)
            liste_init = copy.deepcopy(liste)
            dbl = gagne - bl+croc3
            (t4,gl,croc4,cle4)=g(i,j,liste_init,imm,gagne, croc, cle)
            dgl = gagne - gl+croc4
            if (liste!=t1 and hl>=0):
                c1=[]
                k1="h"
                c1.append(k1)
                c1.append(dhl)
                cc1=tuple(c1)
                interm.append(cc1)
            else:
                #print("t1 ", conc)
                #print(t1)
                v+=1
            if (liste!=t2 and dl>=0):
                c2=[]
                k1="d"
                c2.append(k1)
                c2.append(ddl)
                cc2=tuple(c2)
                interm.append(cc2)
            else:
                #print("t2 ", conc)
                #print(t2)
                v+=1
            if (liste!=t3 and bl>=0):
                c3=[]
                k1="b"
                c3.append(k1)
                c3.append(dbl)
                cc3=tuple(c3)
                interm.append(cc3)
            else:
                #print("t3 ", conc)
                #print(t3)
                v+=1
            if (liste!=t4 and gl>=0):
                c4=[]
                k1="g"
                c4.append(k1)
                c4.append(dgl)
                cc4=tuple(c4)
                interm.append(cc4)
            else:
                #print("t4 ", conc)
                #print(t4)
                v+=1
                
            if v==4:
                dic[conc]=[]
            else:
                dic[conc]=interm
    return dic

def dic_to_dicIndex(dic):
    dicIndex = {}
    for v in dic:
        dicIndex[v] = []
        for j in range(len(dic[v])):
            current = v
            
            if dic[v][j][0]=="h": #pas besoin de mettre des tests car on sait grâce au dictionnaire quelles actions sont légales
                var=str(int(current[0])-1)+current[1]
            elif dic[v][j][0]=="b":
                var=str(int(current[0])+1)+current[1]
            elif dic[v][j][0]=="g":
                var=current[0]+str(int(current[1])-1)
            elif dic[v][j][0]=="d":
                var=current[0]+str(int(current[1])+1)
            dicIndex[v].append(var)
    return dicIndex      


def testEndpoints(pile, endPoints):
    for v in endPoints:
        if v in pile:
            return True
    return False 


def exploreLargeurEtatsVisites(dic, startingPoint, endPoints):#endPoints est une liste des différents endPoints
    #les points doivent être sous la forme : "ij", ex : startingPoint="45"
    #print("RECHERCHE LARGEUR AVEC ETATS VISITES")
    pile = [startingPoint]
    explored = []
    #print(f"Pile : {pile}, Visités : {explored}")
    dicIndex = dic_to_dicIndex(dic)
    while (not testEndpoints(pile, endPoints) and pile!=[]):
        current = pile.pop(0)
        explored.append(current)
        for succ in dic[current]:
            if succ[0]=="h": #pas besoin de mettre des tests car on sait grâce au dictionnaire quelles actions sont légales
                var=str(int(current[0])-1)+current[1]
            elif succ[0]=="b":
                var=str(int(current[0])+1)+current[1]
            elif succ[0]=="g":
                var=current[0]+str(int(current[1])-1)
            elif succ[0]=="d":
                var=current[0]+str(int(current[1])+1)
            if var not in explored:
                pile.append(var)
        
        
    #print(f"Pile : {pile}, Visités : {explored}")
    ch=[]
    chemin=[]
    chemin_action=[]
    ch.append(explored[len(explored)-1])
    i=len(explored)-1 #l'index du père courrant
    k=len(explored)-2 #l'index du descendant

    while i!=0 and k!=-1:
        if explored[k] in dicIndex[explored[i]] or explored[i] in dicIndex[explored[k]]:
            ch.append(explored[k])
            i=k
            k=k-1
        else:
            k=k-1
    for i in range(0,len(ch)):
        chemin.insert(0,ch[i])
    
    for i in range(len(endPoints)):
        if endPoints[i] not in chemin:
            chemin.append(endPoints[i])

    if startingPoint not in chemin:
        chemin.insert(0,startingPoint)

    for i in range(len(chemin)-1):
        chemin_action.append(getActionFromIndexes(chemin[i],chemin[i+1]))

    #print(f'Solution: {chemin, chemin_action}')
    return chemin, chemin_action


def getActionFromIndexes(origine, target):
    x1 = int(origine[0])
    y1 = int(origine[1])
    x2 = int(target[0])
    y2 = int(target[1])
    if(x1 < x2):
        return "b"
    if(x1 > x2):
        return "h"
    if(y1 < y2):
        return "d"
    if(y1 > y2):
        return "g"

# si on pousse un rocher, 
# en general, toujours mettre à jour la matrice

def Astar(laby, startingPoint, endPoint):
    #print("RECHERCHE PROFONDEUR - A* ")
    explored=[]
    poids_current=0
    somme = 0
    file = [(startingPoint, somme)]
    fileSommets = [startingPoint]
    explored.append(startingPoint)
    dicIndex = dic_to_dicIndex(laby)
    while endPoint not in fileSommets and file != []:
        (current, poids_current) = file.pop(0)
        #print("############",current)
        for succ in laby[current]:
            if succ[0]=="h": #pas besoin de mettre des tests car on sait grâce au dictionnaire quelles actions sont légales
                var=str(int(current[0])-1)+current[1]
            elif succ[0]=="b":
                var=str(int(current[0])+1)+current[1]
            elif succ[0]=="g":
                var=current[0]+str(int(current[1])-1)
            elif succ[0]=="d":
                var=current[0]+str(int(current[1])+1)
            poids_successeur=int(succ[1])
            if var not in explored:
                #file.append(var)
                file.append((var, poids_current+poids_successeur))
            fileSommets.append(var)
        file.sort() #on trie la file pour mettre le plus petit poids devant
        if file != []:
            explored.append(file[0][0])
    ch=[]
    chemin=[]
    chemin_action=[]
    ch.append(explored[len(explored)-1]) #on append le endPoint
    i=len(explored)-1 #l'index du père courrant
    k=len(explored)-2 #l'index du descendant
    while i!=0 and k!=-1:
        if explored[k] in dicIndex[explored[i]] or explored[i] in dicIndex[explored[k]]:
            ch.append(explored[k])
            i=k
            k=k-1
        else:
            k=k-1
    for i in range(0,len(ch)):
        chemin.insert(0,ch[i])
    if endPoint not in chemin:
        chemin.append(endPoint)
    if startingPoint not in chemin:
        chemin.insert(0,startingPoint)

    for i in range(len(chemin)-1):
        chemin_action.append(getActionFromIndexes(chemin[i],chemin[i+1]))
    
    #print(f'Solution: {chemin, chemin_action}')
    return chemin, chemin_action
    
def main():
    res = grid_from_file("level7.txt")
    grille=res["grid"]
    init,imm=remplissage_grilles(dicoinit,dicoimm,grille)
    gagne=res["max_steps"]
    croc=0
    cle=False
    #algo de recherche avec init imm gagne croc et cle
    #on lance verif_plan avec la liste d'action retourné par l'algo de recherche

    dico = dico_voisins_satisfiables(init,imm,gagne, croc, cle)


    # path to the key
    ch_key,la_key = Astar(dico,"56",findTarget(imm,"K")[0])
    if la_key != []:
        cle = True
    ch, la = Astar(dico,str(findTarget(imm,"K")[0]),"24")

    la = la_key+la

    if verif_plan(la,init,imm,gagne,croc,cle) == True:
        print("True")
    else:
        print("False")

    texte=""
    for lettre in la:
        texte+=lettre
    print(texte)
    return texte
    
main()


