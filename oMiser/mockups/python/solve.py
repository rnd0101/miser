# -*- coding: utf-8 -*-

"""
Random / brute force solver to find miser scripts with given condition
"""
from random import choice

from miser import c, E, ARG, C, e, NIL, EV, D, B, SELF, A, L, ap
from library import cK, cS


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
            EV,
            # cK,
            # cS,
            # SELF,
        ]
    }

    groups = "binops", "unops", "leafs"
    if max_level == 1:
        groups = "leafs",

    script = None
    op_group = choice(groups)
    op = choice(config[op_group])
    if op_group == "binops":
        script = op(builder(max_level - 1, visitor), builder(max_level - 1, visitor))
    elif op_group == "unops":
        script = op(builder(max_level - 1, visitor))
    else:
        script = op
    visitor(script, top)

    return script


def do_apply_args(p, lst):
    for arg in lst:
        p = ap(p, arg)
    return p


# Some obs
x = L("x")
y = L("y")
z = L("z")
t = L("t")


if __name__ == "__main__":
    def visitor(ob, top):
        return

    rules = [
        (
            [x ** (y ** z)],
            (x ** y) ** z
        )
    ]

    seen = set()
    solutions = []
    max_level = 2
    min_solution = 1000000
    infs = 0
    while not solutions:
        print "Level: {} Inf: {}".format(max_level, infs)
        max_level += 1
        for i in xrange(max_level * 20000):
            s = builder(max_level, visitor, top=True)
            if s in seen:
                continue
            if max_level < 6:
                seen |= {s}
            try:
                if all(do_apply_args(s, r[0]) == r[1] for r in rules):
                    if len(str(s)) < min_solution:
                        print
                        print s
                        min_solution = len(str(s))
                        solutions.append(s)
            except RuntimeError:
                # print ("Infinite loop: {}".format(s))
                infs += 1

        if max_level > 50:
            break
