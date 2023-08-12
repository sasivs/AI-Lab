rread(john).
wealthy(john).
smart(X):- rread(X).
happy(X):- wealthy(X), smart(X).
exciting(X):- happy(X).

studies(john, _):- false.
lucky(john).
lottery(X):- lucky(X).
pass(X,Y):- studies(X,Y); lucky(X).
happys(X):- pass(X,history), lottery(X).



