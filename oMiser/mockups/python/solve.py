# -*- coding: utf-8 -*-

"""
Random / brute force solver to find miser scripts with given condition
"""
from random import choice

from miser import c, E, ARG, C, e, NIL, EV, D, B, SELF, A, L, ap


def builder(max_level, visitor, top=False, config=None):
    config = config or {
        "binops": [c],
        "unops": [e],
        "leafs": [
            ARG,
            A,
            B,
            C,
            D,
            E,
            NIL,
            EV
        ]  # SELF
    }

    groups = "binops", "unops", "leafs"
    if max_level == 1:
        groups = "leafs",

    script = None
    op_group = choice(groups)
    op = choice(config[op_group])
    if op_group == "binops":
        script = op(builder(max_level-1, visitor), builder(max_level-1, visitor))
    elif op_group == "unops":
        script = op(builder(max_level-1, visitor))
    else:
        script = op
    visitor(script, top)

    return script

if __name__ == "__main__":
    def visitor(ob, top):
        return

    rules = [
        (
#            c(L("x"), c(L("y"), L("z"))),
#            c(c(L("x"), L("y")), L("z"))

#            c(L("x"), L("y")),
#            c(L("y"), L("x"))

            e(L("x")),
            c(L("x"), L("x"))
         ),
    ]

    all = set()
    solutions = []
    max_level = 4
    min_solution = 1000000
    while not solutions:
        max_level += 2
        for i in xrange(1000000):
            s = builder(max_level, visitor, top=True)
            if s in all:
                continue
            all |= {s}
            try:
                if any(ap(s, r[0]) == r[1] for r in rules):
                    if len(str(s)) < min_solution:
                        print s
                        min_solution = len(str(s))
                        solutions.append(s)
                        print
            except RuntimeError:
                #print ("Infinite loop: {}".format(s))
                print

        if max_level > 50:
            break
