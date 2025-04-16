# 🧠 Projet IA Logique – Résolution du jeu *Helltaker*

Ce projet propose une approche logique et algorithmique de résolution du jeu *Helltaker*, un jeu de réflexion de type sokoban où le joueur doit planifier des déplacements pour atteindre une fin de niveau tout en respectant des contraintes.  

Exploration de plusieurs formalismes logiques et méthodes d’IA pour résoudre les niveaux du jeu, en deux parties :  

- Une **modélisation STRIPS** pour comprendre et formaliser les actions et états.
- Une résolution complète des **9 niveaux en ASP** (Answer Set Programming).

---

## 📁 Structure du projet

- **ASP/**
  - **helltaker_asp.lp** : Programme ASP (règles et faits)
  - **asp.py** : Script Python pour lancer la résolution des niveaux par ASP
- **levels/**
    - **level1.txt ... level9.txt** : Les 9 niveaux du jeu à résoudre
- **STRIPS/**
    - **Annexes_STRIPS.pdf** : Formalisation du problème avec STRIPS
- **Compte_rendu_final.pdf** : Compte rendu du projet
- **README.md** : Présentation du projet (ce fichier)  

---

## 📘 Partie STRIPS

Cette partie modélise les actions du jeu Helltaker selon le formalisme STRIPS.  
Consulter le fichier `Annexes_STRIPS.pdf` pour les détails.

---

## 🧮 Partie ASP – Résolution Logique

- Résolution des niveaux via ASP avec le solveur Clingo.
- Lancement du fichier `helltaker_asp.lp` via le fichier `asp.py`, pour résoudre les 9 niveaux.

### 🔧 Utilisation

1. Exécuter le script :

```bash
python3 ASP/asp.py
```
2. Choisir le niveau à résoudre (entre 1 et 9).

Le programme affichera :
- `ok` pour indiquer que la solution trouvée est correcte.  
- La séquence d’actions à réaliser pour résoudre le niveau (avec `h` pour haut, `b` pour bas, `g` pour gauche, `d` pour droite).  


### 💡 Détails techniques

Le fichier `helltaker_asp.lp` contient les règles et faits nécessaires pour modéliser les différents états du jeu et les actions possibles.  
Le solveur **Clingo** est utilisé pour générer la solution du niveau en résolvant le programme ASP.  
Le script **asp.py** permet d'exécuter Clingo et d'afficher la séquence d'actions à effectuer pour atteindre la solution du niveau.

