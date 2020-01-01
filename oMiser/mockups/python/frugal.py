# -*- coding: utf-8 -*-

from parsimonious import Grammar, NodeVisitor
from parsimonious.grammar import RuleVisitor


frugal_grammar = Grammar(r"""
    program = command / equation_statement / statement_seq
    statement_seq = space? statement (";" space? statement)*
    statement = assignment / expression
    assignment = "ob" space new_var space? "=" space? expression space?
    command = ("graph" / "include" / "eval" / "debug") (space ~".+"i)?
    equation_statement = "solve" equation+
    equation = space new_var space? expression space? "==" space? expression space? ";"
    expression = space? primary (space? primary)* space?
    primary = term (space? "::" space? term)*
    term = primitive / lindy / var / enclosure / subterm / list
    primitive = ".ARG" / ".A" / ".B" / ".C" / ".D" / ".EV" / ".E" / ".SELF" / ".NIL" / ~"[.][a-zA-Z0-9]+"
    enclosure = ~"`|‵" space? term
    subterm = "(" list_item ("," list_item)* ")"
    list = "[" list_item ("," list_item)* "]"
    list_item = space? expression space?
    lindy = ~"[A-Za-z0-9]+"i
    new_var = "^" ~"[a-zA-Z0-9]+"i
    var = "^" ~"[a-zA-Z0-9]+"i
    quote = "\""
    space = ~"\s+"i
    comment_begin = "(*"
    comment_end = "*)"
    comment = comment_begin comment_inside* comment_end
    comment_inside = comment / (!comment_begin !comment_end ~".")
    """)

class ArgumentList(object):
    """Structure for arguments. Dirty hack to get around lack of encoding for `f(x,y,z)` style"""
    def __init__(self, t):
        self._t = t

    def get(self):
        return self._t

    def __str__(self):
        return str(self._t)

    def __repr__(self):
        return "(" + ", ".join(str(t) for t in self._t) + ")"


class Command(object):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class Equation(object):
    def __init__(self, args, result, varname):
        self.args = args
        self.result = result
        self.varname = varname


def consify(ctx, lst):
    """Given a list, construct pairs starting from the end"""
    if len(lst) == 1:
        return lst[0]
    if len(lst) == 2:
        return ctx['c('](lst[-2], lst[-1])
    return consify(ctx, lst[:-2] + [consify(ctx, lst[-2:])])


def do_apply(ctx, lst):
    """Given a list, do apply"""
    if len(lst) == 1:
        return lst[0]
    if len(lst) == 2:
        return ctx['ap('](lst[-2], lst[-1])
    return do_apply(ctx, lst[:-2] + [do_apply(ctx, lst[-2:])])


def do_apply_args(ctx, p, lst):
    """Given a function and arguments, do apply in normal order"""
    for arg in lst.get():
        p = ctx['ap('](p, arg)
    return p

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

    def visit_equation_statement(self, node, children):
        _, tail = children
        return tail

    def visit_expression(self, node, children):
        _, head, tail, _ = children
        if type(tail) != list:
            tail = []
        seq = [head] + [i[1] for i in tail]
        if len(seq) > 1 and isinstance(seq[1], ArgumentList):
            res = do_apply_args(self.ctx, seq[0], seq[1])
        else:
            res = do_apply(self.ctx, seq)   # This applies right away. TODO: structure first, then frugal-side eval/ap
        return res

    def visit_statement(self, node, children):
        st, = children
        return st

    def visit_command(self, node, children):
        name, args = children
        if type(args) == list:
            args = args[0][1].text
        else:
            args = ''
        return Command(name[0].text, args)

    def visit_equation(self, node, children):
        _, varname, _, args, _, _, _, result, _, _ = children
        if isinstance(args, ArgumentList):
            args = args.get()
        else:
            args = [args]
        return Equation(args, result, varname)

    def visit_assignment(self, node, children):
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
        if len(seq) < 2:
            return seq[0]
        return ArgumentList(seq)

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
        return self.ctx['L('](node.text)


def frugal_to_tree(frugal_expression, ctx):
    return FrugalVisitor(ctx).parse(frugal_expression)


def test():
    import miser as obap
    print((frugal_to_tree('.C `.C (.C (.E  .C (.E .ARG) `.ARG) `(.C (.E .ARG) `.ARG) )', obap)))
