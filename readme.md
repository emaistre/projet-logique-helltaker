Partie python
Cette partie correspond au document « Codes_python_IA02.py »
Pour pouvoir obtenir une solution, on peut faire les commandes suivantes :
dico=dico_voisins_satisfiables(init,imm,32, 0, False)
print(Astar(dico, "56", "24"))
Cela nous renverra deux listes. 
Une avec les différentes actions à réaliser pour atteindre le but final sous la forme [“h”,”h”,”g”,”d”].
L’autre liste renvoie les cases sur lesquelles aller et correspondants à ces actions sous la forme : [“56”, “45”, “78”] (c'est-à-dire ligne i=5 et colonne j=6 etc).
Partie ASP
Fichier asp.py à lancer pour avoir la liste d'étape.
Modifier pour sélectionner le niveau dans le main.
Il lancera helltaker_asp.lp.