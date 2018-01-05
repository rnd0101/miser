grammar Miser;
program : ob '.';
ob : i | '(' ob ')' | pair | enclosure;
pair : '(' ob C ob ')';
enclosure : D ob;
i : individual | primitive | lindy | evbinop | evunop | evref;
individual : I;
primitive : P;
evref : EVREF;
evbinop : EVBINOP;
evunop : EVUNOP;
EVBINOP : 'C' | 'D';
EVUNOP : 'EV';
EVREF : 'SELF' | 'ARG' ;
I : [a-z]+;
P : 'NIL' | 'A' | 'B' | 'E' ;
D : '`';
C : '::';
lindy : LINDY;
LINDY : '"' [a-zA-Z0-9_]+ '"';
WS : [ \t\r\n]+ -> skip ;
