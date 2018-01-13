# -*- coding: utf-8 -*-

from parsimonious import Grammar

frugal_grammar = Grammar(r"""
    program = term ((space* cons? space*) term)*
    term = primitive / ( quote lindy quote ) / ( tick term ) / ( open space* program space* close)
    primitive = ".ARG" / ".A" / ".B" / ".C" / ".D" / ".EV" / ".E" / ".SELF" / ".NIL"
    quote = "\""
    tick = "`"
    cons = "::"
    open = "("
    close = ")"
    lindy = ~"[A-Za-z0-9]+"i
    space = ~"\s+"i
    """)

print(frugal_grammar.parse(".A .B"))
print(frugal_grammar.parse('"lll"'))
print(frugal_grammar.parse('"lll"::.B'))

print(frugal_grammar.parse('.C `.C (.C (.E  .C (.E .ARG) `.ARG) `(.C (.E .ARG) `.ARG) )'))

#     tick = "`"
# ( primitive / quote lindy quote / "(" program ")" )