from fileinput import filename
from pprint import pprint
import sys
import os
from typing import List
from tabnanny import check
import clingo

# Fonction qui complète toutes les lignes d'une matrice 'm' pour qu'elles aient la même longueur 'n'
def complete(m: List[List[str]], n: int):
    for l in m:
        for _ in range(len(l), n):
            l.append(" ") # Ajoute des espaces vides à la fin des lignes trop courtes
    return m

# Fonction qui convertit une grille de caractères en une grille traduite via un dictionnaire 'voc'
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
                title = l # Première ligne : titre du niveau
                continue
            if no == 2:
                max_steps = int(l) # Deuxième ligne : nombre de pas max
                continue

            if len(l) > n:
                n = len(l) # Mise à jour de la largeur max
                complete(grid, n)

            if l != "":
                grid.append(list(l))

    m = len(grid) # Nombre de lignes

    return {"grid": grid, "title": title, "m": m, "n": n, "max_steps": max_steps}

# Fonction de test
def test():
    if len(sys.argv) != 2:
        sys.exit(-1)

    filename = sys.argv[1]
    pprint(grid_from_file(filename, {"H": "@", "B": "$", "D": "."}))
    print(check_plan("erfre"))
    print(check_plan("hhbbggdd"))

# Dictionnaire de traduction des caractères de la grille vers des faits ASP
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

# Transforme la grille en faits ASP à partir du dictionnaire dico, en ajoutant au programme pb
# Écrit dans le fichier temporaire seulement s'il faut satisfaire une dépendance externe
def tranformation(dico,gille,file,pb):
    file = open(file, "w")
    for x in range(len(grille)):
        for y in range(len(gille[x])):
            if grille[x][y]!="#": # On ignore les murs
                for mot in dico[grille[x][y]]:
                    texte=mot.replace("_",f"{x},{y}")
                    # file.write(f"{texte}.\n") #si on veut l'afficher dans un fichier
                    pb+=f"{texte}.\n"
    file.close()
    return pb

# Fonction qui exécute Clingo sur un programme ASP donné (pb), pour un nombre max de pas (n)
def cling(pb,n): 
    la = [None] * (n) # Initialise une liste pour les actions par pas
    ctl = clingo.Control()
    ctl.add("base", [], pb)
    ctl.ground([("base", [])])
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            for atom in model.symbols(atoms=True):
                if atom.match("do", 2):
                    pas = atom.arguments[0]#le pas
                    rang = atom.arguments[1].number#l'etape
                    la[rang] = str(pas)
        if handle.get().unsatisfiable:
            return False, la # Aucun plan trouvé

    # Filtre les actions inutiles
    la2=[]
    for i in range (0, len(la)):
        if la[i] != "p" and la[i] != "nop":
            la2.append(la[i])
    return True, la2
    

if __name__ == "__main__":
    # Demander à l'utilisateur un niveau entre 1 et 9
    level = int(input("Entrez un niveau entre 1 et 9 : "))
    while not (1 <= level <= 9):
        print("Le nombre n'est pas entre 1 et 9.")
        level = int(input("Entrez un niveau entre 1 et 9 : "))
    print(f"Niveau {level}")

    # Obtenir le chemin absolu du dossier contenant le script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Lecture de la grille correspondant au niveau choisi
    res = grid_from_file(os.path.join(base_dir, "..", "levels", f"level{level}.txt"))
    grille = res["grid"]

    # Création de la base ASP avec le nombre de pas et transformation de la grille au format asp
    pb = f"#const n={res['max_steps']}.\n"
    pb = tranformation(dico, grille, "test5.lp", pb)

    with open('ASP/helltaker_asp.lp','r') as f:
        for line in f: 
            pb += line

    # Suppression du fichier temporaire généré
    if os.path.exists("test5.lp"):
        os.remove("test5.lp")

    # Appel du solveur Clingo avec la base ASP générée
    bool, la = cling(pb, res['max_steps'])

    # Affichage du résultat
    if bool:
        # On retourne la liste d'action concaténée comme demandé
        texte = ''.join(la)
        print("ok", texte)
    else:
        print("Unsatisfaible")
