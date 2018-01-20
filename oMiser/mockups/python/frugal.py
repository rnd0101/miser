# -*- coding: utf-8 -*-

from parsimonious import Grammar, NodeVisitor
from parsimonious.grammar import RuleVisitor

frugal_grammar = Grammar(ur"""
    program = statement_seq
    statement_seq = space? statement (";" space? statement)*
    statement = assignment / expression
    assignment = "ob" space new_var space? "=" space? expression space?
    expression = space? primary (space primary)* space?
    primary = term (space? "::" space? term)*
    term = primitive / lindy / var / enclosure / subterm / list
    primitive = ".ARG" / ".A" / ".B" / ".C" / ".D" / ".EV" / ".E" / ".SELF" / ".NIL" / ~"[.][a-zA-Z0-9]+"
    enclosure = ~"`|‵" space? term
    subterm = "(" list_item ("," list_item)* ")"
    list = "[" list_item ("," list_item)* "]"
    list_item = space? expression space?
    lindy = quote ~"[A-Za-z0-9]+"i quote
    new_var = "^" ~"[a-zA-Z0-9]+"i
    var = "^" ~"[a-zA-Z0-9]+"i
    quote = "\""
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
    visit_program = NodeVisitor.lift_child

    def __init__(self, context):
        self.ctx = context

    def visit_statement_seq(self, node, children):
        _, head, tail = children
        if type(tail) != list:
            tail = []
        seq = [head] + [i[2] for i in tail]
        return seq

    def visit_expression(self, node, children):
        _, head, tail, _ = children
        if type(tail) != list:
            tail = []
        seq = [head] + [i[1] for i in tail]
        return consify(self.ctx, seq)  # TODO: application instead

    def visit_statement(self, node, children):
        st, = children
        return st

    def visit_assignment(self, node, children):
        # "ob" space var space? "=" space? expression space?
        _, _, varname, _, _, _, exp, _ = children
        return (varname, exp)

    def visit_primary(self, node, children):
        head, tail = children
        if type(tail) != list:
            tail = []
        seq = [head] + [i[3] for i in tail]
        return consify(self.ctx, seq)

    def visit_primitive(self, node, children):
        primitive, = children
        return self.ctx[primitive.text]

    def visit_subterm(self, node, children):
        _, head, tail, _ = children
        if type(tail) != list:
            return head
        seq = [head] + [i[1] for i in tail]
        return consify(self.ctx, seq)   # TODO: application participant

    def visit_enclosure(self, node, children):
        _, _, term = children
        return self.ctx['e('](term)

    def visit_var(self, node, children):
        _, varname = children
        return self.ctx[varname.text]  # TODO: caution

    def visit_new_var(self, node, children):
        _, varname = children
        return varname.text

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
