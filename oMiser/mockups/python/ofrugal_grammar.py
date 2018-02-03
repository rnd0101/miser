# -*- coding: utf-8 -*-

import lark

parser = lark.Lark(
u"""

// 3. TEXT, CHARACTERS, SPACING, AND CONCRETE LAYOUT CONSIDERATIONS

LINDY: /[a-zA-Z0-9_]+\w*/
PRIMITIVE: /\.[a-zA-Z0-9_]+\w*/ 
BINDING_NAME: /\^[a-zA-Z0-9_]+\w*/ 

// 4. TERMS

term: LINDY
    | PRIMITIVE
    | BINDING_NAME

//    [DETAILS TBD]

// 5. LIST FORMS

list_body: ob_exp "]"
    | ob_exp ":]"
    | ob_exp "," list_body

list_form: "[" "]"
    | "[" list_body

// 6. FUNCTIONAL FORMS

function_form:  term 
    | function_form list_form
    | function_form "(" arguments ")"

obap_form: "(" ob_exp ")" 
    | obap_form list_form 
    | obap_form "(" arguments ")"

arguments: ob_exp 
    | arguments "," ob_exp

// 7. UNARIES

unary: function_form 
    | "‵" obap_form 
    | "‵" unary     

// 8. APPLICATIVE EXPRESSIONS

ae_form: unary | unary ae_form
ae: ae_form | obap_form ae_form

// 9. OB_EXP

binary: ae | ae "::" binary

ob_exp: binary


%import common.WS
%ignore WS
""", start='ob_exp'
)
