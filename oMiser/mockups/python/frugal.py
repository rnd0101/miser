# -*- coding: utf-8 -*-

from parsimonious import Grammar, NodeVisitor
from parsimonious.grammar import RuleVisitor

frugal_grammar = Grammar(ur"""
    program = space? term cons* space?
    cons = space? "::"? space? term
    term = primitive / lindy / enclosure / subterm / list
    primitive = ".ARG" / ".A" / ".B" / ".C" / ".D" / ".EV" / ".E" / ".SELF" / ".NIL" / ~"[.][a-zA-Z]+"  
    quote = "\""
    enclosure = ~"`|‵" space? term
    subterm = "(" space? program space? ")"
    list = "[" list_item ("," list_item)* "]"
    list_item = space? program space?
    lindy = quote ~"[A-Za-z0-9]+"i quote
    space = ~"\s+"i
    comment_begin = "(*"
    comment_end = "*)"
    comment = comment_begin comment_inside* comment_end
    comment_inside = comment / (!comment_begin !comment_end ~".")
    """)


def consify(ctx, lst):
    """Given a list, construct pairs starting from the end"""
    if len(lst) == 1:
        return lst[0]
    if len(lst) == 2:
        return ctx['c('](lst[-2], lst[-1])
    return consify(ctx, lst[:-2] + [consify(ctx, lst[-2:])])


class FrugalVisitor(RuleVisitor):
    grammar = frugal_grammar

    def __init__(self, context):
        self.ctx = context

    def visit_primitive(self, node, children):
        primitive, = children
        return self.ctx[primitive.text]

    def visit_cons(self, node, children):
        _, _, _, term = children
        return term

    def visit_subterm(self, node, children):
        _, _, term, _, _ = children
        return term

    def visit_enclosure(self, node, children):
        _, _, term = children
        return self.ctx['e('](term)

    def visit_program(self, node, children):
        _, head, tail, _ = children
        if type(tail) != list:
            tail = []
        seq = [head] + tail
        return consify(self.ctx, seq)

    def visit_list(self, node, children):
        _, head, tail, _ = children
        if type(tail) != list:
            tail = []
        seq = [head] + [i[1] for i in tail]
        return consify(self.ctx, seq)

    def visit_list_item(self, node, children):
        return children[1]

    def visit_lindy(self, node, children):
        _, s, _ = children
        return self.ctx['L('](s.text)


def frugal_to_tree(frugal_expression, ctx):
    return FrugalVisitor(ctx).parse(frugal_expression)


def test():
    import miser as obap
    print(frugal_to_tree('.C `.C (.C (.E  .C (.E .ARG) `.ARG) `(.C (.E .ARG) `.ARG) )', obap))
