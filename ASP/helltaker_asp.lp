
etape(0..n-1).
action(h;b;d;g;nop;p).

fluent(F, 0) :- init(F). %l'etat initial nous donne un fluent de l'etape 0

but(robot(X-1,Y)) :- init(fille(X,Y)),case(X-1,Y).
but(robot(X+1,Y)) :- init(fille(X,Y)),case(X+1,Y).
but(robot(X,Y-1)) :- init(fille(X,Y)),case(X,Y-1).
but(robot(X,Y+1)) :- init(fille(X,Y)),case(X,Y+1).

achieved(T) :- fluent(F, T), but(F).

:- not achieved(_). % on doit finir
:- achieved(T), T > n. % on doit finir avant n
:- achieved(T), do(Act, T), Act != nop. % la seule action possible une fois qu'on a fini : nop
:- do(nop, T), not achieved(T). % mais on ne peut faire nop qu'une fois qu'on a fini

%%% générateur d'actions..
{ do(Act, T): action(Act) } = 1 :- etape(T).

%action cle/tresor
supprime(cle(X,Y),T):-
    fluent(cle(X, Y), T),
	fluent(robot(X, Y), T).
supprime(tresor(X,Y),T):-
    fluent(tresor(X, Y), T),
	fluent(robot(X, Y), T).
trouve(clef):-
	fluent(cle(X, Y), T),
	fluent(robot(X, Y), T).

%action pic non variable
fluent(robot(X,Y),T+1) :-
	do(p, T),
	fluent(robot(X,Y),T),
	fluent(croc(X,Y),T).
	
:- 	fluent(robot(X,Y),T),
	fluent(croc(X,Y),T),
	not do(p,T-1),
	not do(p,T).
	
supprime(zombie(X,Y),T):-
	fluent(zombie(X,Y),T),
	fluent(croc(X,Y),T).

%action pic variables
%impairs

fluent(crocimpair(X,Y),T+1):-
	fluent(crocpair(X,Y),T),
	T+1<n,
	not do(p,T).
supprime(crocimpair(X,Y),T):-
	fluent(crocimpair(X,Y),T),
	not do(p,T).
fluent(crocimpair(X,Y),T+1):-
	fluent(crocimpair(X,Y),T),
	T+1<n, do(p,T).
	
:- 	fluent(robot(X,Y),T),
	fluent(crocimpair(X,Y),T),
	not do(p,T-1),
	not do(p,T).
	
supprime(zombie(X,Y),T):-
	fluent(zombie(X,Y),T),
	fluent(crocimpair(X,Y),T).
fluent(crocpair(X,Y),T+1):-
	fluent(crocpair(X,Y),T),
	T+1<n, do(p,T).	
	
%pairs
fluent(crocpair(X,Y),T+1):-
	fluent(crocimpair(X,Y),T),
	T+1<n,
	not do(p,T).
supprime(crocpair(X,Y),T):-
	fluent(crocpair(X,Y),T),
	not do(p,T).

	
%%% les actions
%%  action gauche
% précondition
:-  do(g, T), 
    fluent(robot(X, Y), T), 
    not case(X, Y-1). 
:-  do(g, T), 
    fluent(robot(X, Y), T), 
	fluent(tresor(X,Y-1),T),
    not trouve(clef).
	

% effets
fluent(robot(X, Y - 1), T + 1) :-
    do(g, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X,Y-1),T),
	not fluent(fille(X,Y-1),T),
	not fluent(zombie(X,Y-1),T).
supprime(robot(X, Y), T) :-
    do(g, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X,Y-1),T),
	not fluent(fille(X,Y-1),T),
	not fluent(zombie(X,Y-1),T).
fluent(caisse(X,Y-2),T+1):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X, Y-1), T),
	not fluent(caisse(X, Y-2), T),
	not fluent(fille(X, Y-2), T),
	not fluent(zombie(X,Y-2),T),
	not fluent(tresor(X, Y-2), T),
	case(X,Y-2).
supprime(caisse(X,Y-1),T):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X, Y-1), T),
	not fluent(caisse(X,Y-2), T),
	not fluent(fille(X,Y-2), T),
	not fluent(zombie(X,Y-2),T),
	not fluent(tresor(X,Y-2), T),
	case(X,Y-2).
fluent(zombie(X,Y-2),T+1):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y-1), T),
	not fluent(caisse(X, Y-2), T),
	not fluent(fille(X,Y-2), T),
	not fluent(zombie(X,Y-2),T),
	not fluent(tresor(X,Y-2), T),
	not fluent(croc(X,Y-2), T),
	not fluent(crocimpair(X,Y-2), T),
	case(X,Y-2).
supprime(zombie(X,Y-1),T):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y-1), T),
	not fluent(caisse(X, Y-2), T),
	not fluent(fille(X, Y-2), T),
	not fluent(zombie(X,Y-2),T),
	not fluent(tresor(X,Y-2), T),
	not fluent(croc(X,Y-2), T),
	not fluent(crocimpair(X,Y-2), T),
	case(X,Y-2).
supprime(zombie(X,Y-1),T):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y-1), T),
	fluent(caisse(X, Y-2), T).
supprime(zombie(X,Y-1),T):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y-1), T),
	fluent(fille(X, Y-2), T),
	case(X,Y-2).
supprime(zombie(X,Y-1),T):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y-1), T),
	fluent(zombie(X, Y-2), T),
	case(X,Y-2).
supprime(zombie(X,Y-1),T):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y-1), T),
	fluent(tresor(X, Y-2), T),
	case(X,Y-2).
supprime(zombie(X,Y-1),T):-
	do(g, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y-1), T),
	not case(X,Y-2).
	
supprime(zombie(X,Y-1),T):-
	fluent(zombie(X,Y-1),T),
	fluent(robot(X,Y),T),
	do(g,T),
	fluent(crocimpair(X,Y-2),T), case(X,Y-2).	
supprime(zombie(X,Y-2),T):-
	fluent(zombie(X,Y-1),T),
	fluent(robot(X,Y),T),
	do(g,T),
	fluent(croc(X,Y-2),T), case(X,Y-2).
	
%%  action droite
% précondition
:-  do(d, T), 
    fluent(robot(X, Y), T), 
    not case(X, Y+1). 
:-  do(d, T), 
    fluent(robot(X, Y), T), 
	fluent(tresor(X,Y+1),T),
    not trouve(clef).

% effets
fluent(robot(X, Y+1), T + 1):-
    do(d, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X,Y+1),T),
	not fluent(fille(X,Y+1),T),
	not fluent(zombie(X,Y+1),T).
supprime(robot(X, Y), T) :-
    do(d, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X,Y+1),T),
	not fluent(fille(X,Y+1),T),
	not fluent(zombie(X,Y+1),T).
fluent(caisse(X,Y+2),T+1):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X, Y+1), T),
	not fluent(caisse(X, Y+2), T),
	not fluent(fille(X, Y+2), T),
	not fluent(zombie(X, Y+2), T),
	not fluent(tresor(X, Y+2), T),
	case(X,Y+2).
supprime(caisse(X,Y+1),T):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X, Y+1), T),
	not fluent(caisse(X, Y+2), T),
	not fluent(fille(X, Y+2), T),
	not fluent(zombie(X, Y+2), T),
	not fluent(tresor(X, Y+2), T),
	case(X,Y+2).
fluent(zombie(X,Y+2),T+1):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y+1), T),
	not fluent(caisse(X, Y+2), T),
	not fluent(fille(X, Y+2), T),
	not fluent(zombie(X, Y+2), T),
	not fluent(tresor(X, Y+2), T),
	not fluent(croc(X, Y+2), T),
	not fluent(crocimpair(X, Y+2), T),
	case(X,Y+2).
supprime(zombie(X,Y+1),T):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y+1), T),
	not fluent(caisse(X, Y+2), T),
	not fluent(fille(X, Y+2), T),
	not fluent(zombie(X, Y+2), T),
	not fluent(tresor(X, Y+2), T),
	not fluent(croc(X, Y+2), T),
	not fluent(crocimpair(X, Y+2), T),
	case(X,Y+2).
supprime(zombie(X,Y+1),T):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y+1), T),
	fluent(caisse(X, Y+2), T),
	case(X,Y+2).
supprime(zombie(X,Y+1),T):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y+1), T),
	fluent(fille(X, Y+2), T),
	case(X,Y+2).
supprime(zombie(X,Y+1),T):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y+1), T),
	fluent(zombie(X, Y+2), T),
	case(X,Y+2).
supprime(zombie(X,Y+1),T):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y+1), T),
	fluent(tresor(X, Y+2), T),
	case(X,Y+2).
supprime(zombie(X,Y+1),T):-
	do(d, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X, Y+1), T),
	not case(X,Y+2).

supprime(zombie(X,Y+1),T):-
	fluent(zombie(X,Y+1),T),
	fluent(robot(X,Y),T),
	do(d,T),
	fluent(crocimpair(X,Y+2),T), case(X,Y+2).
supprime(zombie(X,Y+1),T):-
	fluent(zombie(X,Y+1),T),
	fluent(robot(X,Y),T),
	do(d,T),
	fluent(croc(X,Y+2),T), case(X,Y+2).
	
%%  action haut
% précondition
:-  do(h, T), 
    fluent(robot(X, Y), T), 
    not case(X-1, Y). 
:-  do(h, T), 
    fluent(robot(X, Y), T), 
	fluent(tresor(X-1,Y),T),
    not trouve(clef).
% effets
fluent(robot(X-1, Y), T + 1):-
    do(h, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X-1,Y),T),
	not fluent(fille(X-1,Y),T),
	not fluent(zombie(X-1,Y),T).
supprime(robot(X, Y), T) :-
    do(h, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X-1,Y),T),
	not fluent(fille(X-1,Y),T),
	not fluent(zombie(X-1,Y),T).
fluent(caisse(X-2,Y),T+1):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X-1, Y), T),
	not fluent(caisse(X-2, Y), T),
	not fluent(fille(X-2, Y), T),
	not fluent(zombie(X-2, Y), T),
	not fluent(tresor(X-2, Y), T),
	case(X-2,Y).
supprime(caisse(X-1,Y),T):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X-1, Y), T),
	not fluent(caisse(X-2, Y), T),
	not fluent(fille(X-2, Y), T),
	not fluent(zombie(X-2, Y), T),
	not fluent(tresor(X-2, Y), T),
	case(X-2,Y).
fluent(zombie(X-2,Y),T+1):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X-1, Y), T),
	not fluent(caisse(X-2, Y), T),
	not fluent(fille(X-2, Y), T),
	not fluent(zombie(X-2, Y), T),
	not fluent(tresor(X-2, Y), T),
	not fluent(crocimpair(X-2, Y), T),
	not fluent(croc(X-2, Y), T),
	case(X-2,Y).
supprime(zombie(X-1,Y),T):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X-1, Y), T),
	not fluent(caisse(X-2, Y), T),
	not fluent(fille(X-2, Y), T),
	not fluent(zombie(X-2, Y), T),
	not fluent(tresor(X-2, Y), T),
	not fluent(crocimpair(X-2, Y), T),
	not fluent(croc(X-2, Y), T),
	case(X-2,Y).
supprime(zombie(X-1,Y),T):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X-1, Y), T),
	fluent(caisse(X-2, Y), T),
	case(X-2,Y).
supprime(zombie(X-1,Y),T):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X-1, Y), T),
	fluent(fille(X-2, Y), T),
	case(X-2,Y).
supprime(zombie(X-1,Y),T):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X-1, Y), T),
	fluent(zombie(X-2, Y), T),
	case(X-2,Y).
supprime(zombie(X-1,Y),T):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X-1, Y), T),
	fluent(tresor(X-2, Y), T),
	case(X-2,Y).
supprime(zombie(X-1,Y),T):-
	do(h, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X-1, Y), T),
	not case(X-2,Y).
	
supprime(zombie(X-1,Y),T):-
	fluent(zombie(X-1,Y),T),
	fluent(robot(X,Y),T),
	do(h,T),
	fluent(crocimpair(X-2,Y),T), case(X-2,Y).
supprime(zombie(X-1,Y),T):-
	fluent(zombie(X-1,Y),T),
	fluent(robot(X,Y),T),
	do(h,T),
	fluent(croc(X-2,Y),T), case(X-2,Y).
	
%%  action bas
% précondition
:-  do(b, T), 
    fluent(robot(X, Y), T), 
    not case(X+1, Y). 
:- 	do(b, T), 
	fluent(tresor(X+1, Y), T),
	fluent(robot(X, Y), T),
	not trouve(clef).
	
% effets
fluent(robot(X+1, Y), T + 1):-
    do(b, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X+1,Y),T),
	not fluent(fille(X+1,Y),T),
	not fluent(zombie(X+1,Y),T).
supprime(robot(X, Y), T) :-
    do(b, T),
    fluent(robot(X, Y), T),
	not fluent(caisse(X+1,Y),T),
	not fluent(fille(X+1,Y),T),
	not fluent(zombie(X+1,Y),T).
fluent(caisse(X+2,Y),T+1):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X+1, Y), T),
	not fluent(caisse(X+2, Y), T),
	not fluent(fille(X+2, Y), T),
	not fluent(zombie(X+2, Y), T),
	not fluent(tresor(X+2, Y), T),
	case(X+2,Y).
supprime(caisse(X+1,Y),T):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(caisse(X+1, Y), T),
	not fluent(caisse(X+2, Y), T),
	not fluent(fille(X+2, Y), T),
	not fluent(zombie(X+2, Y), T),
	not fluent(tresor(X+2, Y), T),
	case(X+2,Y).
fluent(zombie(X+2,Y),T+1):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X+1, Y), T),
	not fluent(caisse(X+2, Y), T),
	not fluent(fille(X+2, Y), T),
	not fluent(zombie(X+2, Y), T),
	not fluent(tresor(X+2, Y), T),
	not fluent(croc(X+2,Y),T),
	not fluent(crocimpair(X+2,Y),T),
	case(X+2,Y).
supprime(zombie(X+1,Y),T):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X+1, Y), T),
	not fluent(caisse(X+2, Y), T),
	not fluent(fille(X+2, Y), T),
	not fluent(zombie(X+2, Y), T),
	not fluent(tresor(X+2, Y), T),
	not fluent(croc(X+2,Y),T),
	not fluent(crocimpair(X+2,Y),T),
	case(X+2,Y).
supprime(zombie(X+1,Y),T):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X+1, Y), T),
	fluent(caisse(X+2, Y), T),
	case(X+2,Y).
supprime(zombie(X+1,Y),T):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X+1, Y), T),
	fluent(fille(X+2, Y), T),
	case(X+2,Y).
supprime(zombie(X+1,Y),T):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X+1, Y), T),
	fluent(zombie(X+2, Y), T),
	case(X+2,Y).
supprime(zombie(X+1,Y),T):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X+1, Y), T),
	fluent(tresor(X+2, Y), T),
	case(X+2,Y).
supprime(zombie(X+1,Y),T):-
	do(b, T),
    fluent(robot(X, Y), T),
	fluent(zombie(X+1, Y), T),
	not case(X+2,Y).
	
supprime(zombie(X+1,Y),T):-
	fluent(zombie(X+1,Y),T),
	fluent(robot(X,Y),T),
	do(b,T),
	fluent(crocimpair(X+2,Y),T), case(X+2,Y).
supprime(zombie(X+1,Y),T):-
	fluent(zombie(X+1,Y),T),
	fluent(robot(X,Y),T),
	do(b,T),
	fluent(croc(X+2,Y),T), case(X+2,Y).

	
%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F, T + 1) :- 
    fluent(F, T), 
    T + 1 < n,
    not supprime(F, T).
	
% après la fin, plus rien ne bouge
fluent(F, T + 1) :-
    fluent(F, T), 
    achieved(T), 
    T + 1 <= n.

#show do/2.