# -*- coding: utf-8 -*-

from parsimonious import Grammar, NodeVisitor
from parsimonious.grammar import RuleVisitor

frugal_grammar = Grammar(ur"""
    program = term cons* space*
    term = primitive / lindy / enclosure / subterm
    primitive = ".ARG" / ".A" / ".B" / ".C" / ".D" / ".EV" / ".E" / ".SELF" / ".NIL" / ~"[.][a-zA-Z]+"  
    quote = "\""
    enclosure = ~"`|‵" term
    cons = space* "::"? space* term
    subterm = "(" space* program space* ")"
    lindy = quote ~"[A-Za-z0-9]+"i quote
    space = ~"\s+"i
    """)


def consify(ctx, lst):
    """Given a list, construct pairs starting from the end"""
    if len(lst) == 1:
        return lst[0]
    if len(lst) == 2:
        return ctx.c(lst[-2], lst[-1])
    return consify(ctx, lst[:-2] + [consify(ctx, lst[-2:])])


class FrugalVisitor(RuleVisitor):
    grammar = frugal_grammar

    def __init__(self, context):
        self.ctx = context

    def visit_primitive(self, node, children):
        primitive, = children
        return getattr(self.ctx, primitive.text.lstrip("."))

    def visit_cons(self, node, children):
        _, _, _, term = children
        return term

    def visit_subterm(self, node, children):
        _, _, term, _, _ = children
        return term

    def visit_enclosure(self, node, children):
        _, term = children
        return self.ctx.e(term)

    def visit_program(self, node, children):
        head, tail, _ = children
        if type(tail) != list:
            tail = []
        seq = [head] + tail
        return consify(self.ctx, seq)

    def visit_lindy(self, node, children):
        _, s, _ = children
        return self.ctx.L(s.text)


def frugal_to_tree(frugal_expression, ctx):
    return FrugalVisitor(ctx).parse(frugal_expression)


def test():
    import miser as obap
    print(frugal_to_tree('.C `.C (.C (.E  .C (.E .ARG) `.ARG) `(.C (.E .ARG) `.ARG) )', obap))
