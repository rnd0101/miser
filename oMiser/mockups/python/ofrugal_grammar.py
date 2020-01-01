# -*- coding: utf-8 -*-

import lark
from lark import Tree
from lark.lexer import Token

parser = lark.Lark(
    """

    // 3. TEXT, CHARACTERS, SPACING, AND CONCRETE LAYOUT CONSIDERATIONS

    LINDY: /[a-zA-Z0-9_]\w*/
    PRIMITIVE: /\.[a-zA-Z0-9_]\w*/
    BINDING_NAME: /\^[a-zA-Z0-9_]\w*/

    // 4. TERMS

    term: LINDY
        | PRIMITIVE
        | BINDING_NAME

    //    [DETAILS TBD]

    // 5. LIST FORMS

    list_body: ob_exp ("," ob_exp)* "]"   -> list_nil
        | ob_exp ("," ob_exp)* ":]"       -> list

    list_form: "[" "]"           -> nil
        | "[" list_body          -> lift

    // 6. FUNCTIONAL FORMS

    function_form:  term                   -> lift
        | function_form list_form          -> application
        | function_form "(" arguments ")"  -> application_with_arguments

    obap_form: "(" ob_exp ")"          -> lift
        | list_form                    -> lift
        | obap_form "(" arguments ")"  -> application_with_arguments

    arguments: ob_exp ("," ob_exp)*

    // 7. UNARIES

    unary: function_form         -> lift
        | ("`" | "‵") obap_form  -> enclosure
        | ("`" | "‵") unary      -> enclosure 

    // 8. APPLICATIVE EXPRESSIONS

    ae_form: unary           -> lift
        | unary ae_form      -> application
    ae: ae_form              -> lift
        | obap_form          -> lift
        | obap_form ae_form  -> application

    // 9. OB_EXP

    binary: ae               -> lift
        | ae "::" binary     -> pair

    ob_exp: binary           -> lift

    // SHELL ADDITIONS

    program: command 
        | equation_statement
        | statement_seq
    ?statement_seq: statement (";" statement)*
    statement: assignment 
       | ob_exp
    assignment: "ob" NEW_VAR "=" ob_exp
    command: COMMAND command_parameters?
    equation_statement: "solve" equation+
    equation: new_var ob_exp "==" ob_exp ";"

    command_parameters: COMMAND_PARAMETERS
    new_var: NEW_VAR

    NEW_VAR: /\^[a-zA-Z0-9_]\w*/
    COMMAND_PARAMETERS: /.+/
    
    // Temprorarily:
    COMMAND: /graph|include|eval|debug/i

    %import common.WS
    %ignore WS
    """, start='program'
)


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


class Interpretation(object):
    def __init__(self, context):
        self.ctx = context

    def __call__(self, arg):
        if isinstance(arg, Tree):
            return getattr(self, arg.data, self._unknown)(arg)
        elif isinstance(arg, Token):
            return getattr(self, arg.type)(arg)

    def LINDY(self, node):
        return self.ctx['L('](node.value)

    def PRIMITIVE(self, node):
        return self.ctx[node.value]

    def BINDING_NAME(self, node):
        return self.ctx[node.value.lstrip('^')]

    def NEW_VAR(self, node):
        return node.value.lstrip('^')

    def COMMAND_PARAMETERS(self, node):
        return node.value

    def COMMAND(self, node):
        return node.value

    def _unknown(self, node):
        return [node.data] + [self(c) for c in node.children]

    def lift(self, node):
        assert len(node.children) == 1
        return self(node.children[0])

    term = lift

    def pair(self, node):
        return self.ctx['c('](self(node.children[0]), self(node.children[1]))

    def enclosure(self, node):
        return self.ctx['e('](self(node.children[0]))

    def application(self, node):
        return self.ctx['ap('](self(node.children[0]), self(node.children[1]))

    def application_with_arguments(self, node):
        p = self(node.children[0])
        for arg in self(node.children[1]):
            p = self.ctx['ap('](p, arg)
        return p

    def arguments(self, node):
        return [self(c) for c in node.children]

    def nil(self, node):
        return self.ctx['.NIL']

    def list_nil(self, node):
        return consify(self.ctx, [self(c) for c in node.children] + [self.ctx['.NIL']])

    def list(self, node):
        return consify(self.ctx, [self(c) for c in node.children])
