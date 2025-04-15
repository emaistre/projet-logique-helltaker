from fileinput import filename
from pprint import pprint
import sys
from typing import List
from tabnanny import check
import clingo


def complete(m: List[List[str]], n: int):
    for l in m:
        for _ in range(len(l), n):
            l.append(" ")
    return m


def convert(grid: List[List[str]], voc: dict):
    new_grid = []
    for line in grid:
        new_line = []
        for char in line:
            if char in voc:
                new_line.append(voc[char])
            else:
                new_line.append(char)
        new_grid.append(new_line)
    return new_grid


def grid_from_file(filename: str):
    """
    Cette fonction lit un fichier et le convertit en une grille de Helltaker

    Arguments:
    - filename: fichier contenant la description de la grille
    - voc: argument facultatif permettant de convertir chaque case de la grille en votre propre vocabulaire

    Retour:
    - un dictionnaire contenant:
        - la grille de jeu sous une forme d'une liste de liste de (chaînes de) caractères
        - le nombre de ligne m
        - le nombre de colonnes n
        - le titre de la grille
        - le nombre maximal de coups max_steps
    """

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


def test():
    if len(sys.argv) != 2:
        sys.exit(-1)

    filename = sys.argv[1]

    pprint(grid_from_file(filename, {"H": "@", "B": "$", "D": "."}))

    print(check_plan("erfre"))
    print(check_plan("hhbbggdd"))



dico={
    "H": ["init(robot(_))", "case(_)"],
    "D": ["init(fille(_))", "case(_)"],
    " ": ["case(_)"],
    "B": ["init(caisse(_))", "case(_)"],
    "K": ["init(cle(_))", "case(_)"],
    "L": ["init(tresor(_))", "case(_)"],
    "M": ["init(zombie(_))", "case(_)"],
    "S": ["init(croc(_))", "case(_)"],
    "U": ["init(crocimpair(_))", "case(_)"],
    "T": ["init(crocpair(_))", "case(_)"],
    "O": ["init(croc(_))", "init(caisse(_))", "case(_)"],
    "Q": ["init(crocimpair(_))", "init(caisse(_))", "case(_)"],
    "P": ["init(crocpair(_))", "init(caisse(_))", "case(_)"],
}
def tranformation(dico,gille,file,pb):
    file = open(file, "w")
    for x in range(len(grille)):
        for y in range(len(gille[x])):
            if grille[x][y]!="#":
                for mot in dico[grille[x][y]]:
                    texte=mot.replace("_",f"{x},{y}")
                    #file.write(f"{texte}.\n") #si on veut l'afficher dans un fichier
                    pb+=f"{texte}.\n"
    file2 = open("hell.lp", "r")
    file.close()
    return pb

def cling(pb,n): #on a tout le programme asp avec pb
    la=[None] * (n) #liste d'action
    ctl = clingo.Control()
    ctl.add("base", [], pb)
    ctl.ground([("base", [])])
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            for atom in model.symbols(atoms=True):
                if atom.match("do", 2):
                    pas=atom.arguments[0]#le pas
                    rang=atom.arguments[1].number#l'etape
                    la[rang]=str(pas)
        if handle.get().unsatisfiable:
            return False,la
    la2=[]
    for i in range (0,len(la)):
        if la[i] != "p" and la[i] != "nop":
            la2.append(la[i])
    return True,la2
    

if __name__ == "__main__":
    res = grid_from_file("level9.txt")
    grille=res["grid"]
    pb=f"#const n={res['max_steps']}.\n"
    pb=tranformation(dico,grille,"test5.lp",pb)
    with open('helltaker_asp.lp','r') as f:
    #, open('test5.lp','a') as s: 
        for line in f: 
            #s.write(line) #si on veut l'ajouter dans un fichier
            pb+=line
    bool,la=cling(pb, res['max_steps'])
    if bool==True:
        #on retourne la liste d'action concaténée comme demandé
        texte=""
        for lettre in la:
            texte+=lettre
        print("ok",texte)
    else:
        print("Unsatisfaible")
