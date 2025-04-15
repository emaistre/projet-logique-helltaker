# 🧠 Projet IA Logique – Résolution du jeu *Helltaker*

Ce projet propose une approche logique et algorithmique de résolution du jeu *Helltaker*, un jeu de réflexion de type sokoban où le joueur doit planifier des déplacements pour atteindre une fin de niveau tout en respectant des contraintes.  

Nous avons exploré plusieurs formalismes logiques et méthodes d’IA pour résoudre les niveaux du jeu, à travers trois grandes parties :  

- Une **modélisation STRIPS** pour comprendre et formaliser les actions et états.
- Une résolution complète des **9 niveaux en ASP** (Answer Set Programming).
- Une résolution basée sur les **espaces d'états et l'algorithme A\*** implémentée en Python.

---

## 📁 Structure du projet

- `Annexes_STRIPS.pdf` – Formalisation du problème avec STRIPS 
- `helltaker_asp.lp` – Programme ASP (règles et faits)  
- `asp.py` – Script Python pour lancer la résolution des niveaux
- `Codes_python_IA02.py` – Résolution via espace d’états et A*
- `Compte_rendu_final.pdf` – Compte rendu du projet
- `level1.txt - ... - level9.txt` – Les 9 niveaux du jeu à résoudre
- `README.md` – Présentation du projet (ce fichier)

---

## 📘 Partie STRIPS

Cette partie modélise les actions du jeu Helltaker selon le formalisme STRIPS.  
Consulter le fichier `Annexes_STRIPS.pdf` pour les détails.

---

## 🧮 Partie ASP – Résolution Logique

- Résolution des niveaux via ASP avec le solveur Clingo.
- Lancement du fichier `helltaker_asp.lp` via le fichier `asp.py`, pour résoudre les 9 niveaux.

### 🔧 Utilisation

1. Modifier le niveau souhaité dans le `main()` de `asp.py`
2. Exécuter le script :

```bash
python asp.py
```
Le programme affichera la séquence d’actions pour résoudre le niveau.

---

## 🐍 Partie Python – A* et Espace d’États

Cette partie utilise une modélisation du jeu sous forme de graphe d’états, résolu avec A*.

### ▶️ Exemple d’utilisation
```python
dico = dico_voisins_satisfiables(init, imm, 32, 0, False)
print(Astar(dico, "56", "24"))
```

### ✅ Sortie

Une liste d’actions à effectuer (ex : ["h", "h", "g", "d"])
Une liste des cases visitées (ex : ["56", "45", "78"])