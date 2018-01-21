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
            c(L("x"), L("y")),
            L("y")
         ),
    ]

    all = set()
    for i in xrange(10000):
        s = builder(20, visitor, top=True)
        if s in all:
            continue
        all |= {s}
        try:
            if any(ap(s, r[0]) == r[1] for r in rules):
                print s
        except RuntimeError:
            print ("Infinite loop: {}".format(s))

