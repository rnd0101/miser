# -*- coding: utf-8 -*-

"""
Random / brute force solver to find miser scripts with given condition
"""
from random import choice

import time

from miser import c, E, ARG, C, e, NIL, EV, D, B, SELF, A, L, ap
from library import cK, cS


def builder(max_level, top=False, config=None):
    groups = "binops", "unops", "leafs"
    if max_level == 1:
        groups = "leafs",

    script = None
    op_group = choice(groups)
    op = choice(config[op_group])
    if op_group == "binops":
        script = op(builder(max_level - 1, config=config), builder(max_level - 1, config=config))
    elif op_group == "unops":
        script = op(builder(max_level - 1, config=config))
    else:
        script = op

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


def solve(rules):
    seen = set()
    solutions = []
    max_level = 3
    min_solution = 1000000
    infs = 0
    dups = 0
    config = {
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
    while not solutions:
        t0 = time.time()
        iters = max_level * 100000
        print("Level: {} Iters: {}".format(max_level, iters))
        max_level += 1
        for i in xrange(iters):
            s = builder(max_level, top=True, config=config)
            if s in seen:
                dups += 1
                continue
            if len(seen) < 2000000:
                seen.add(s)
            try:
                if all(do_apply_args(s, r[0]) == r[1] for r in rules):
                    if len(str(s)) < min_solution:
                        print
                        print s
                        min_solution = len(str(s))
                        solutions.append(s)
            except RuntimeError:
                # print ("Infinite loop: {}".format(s))
                seen.add(s)
                infs += 1

        print("Inf: {} Seen: {} Dups: {} Speed: {} IPS".format(infs, len(seen), dups, iters // (time.time() - t0)))
        if max_level > 20:
            break


if __name__ == "__main__":
    rules = [
 #       (
 #           [x],
 #           (x ** NIL)
 #       ),
#        (
#            [x ** y],
#            (x ** y ** NIL)
#        ),
        (
            [x],
            (x)
        ),
        (
            [x ** y],
            (y ** x)
        ),
#        (
#            [e(x) ** e(y)],
#            (e(y) ** e(x))
#        ),
    ]

    solve(rules)
