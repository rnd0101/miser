# -*- coding: utf-8 -*-

DEBUG = False


class ob(object):
    """Abstract Ob class"""
    name = None
    a = None
    b = None

    @property
    def is_pure_lindy_trace(self):
        return False

    def ap(self, x):
        return c(e(self), e(x))

    def ev(self, p, x):
        return self

    def __pow__(self, other, modulo=None):
        return c(self, other)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__getstate__() == other.__getstate__()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "ob({})".format(repr(self.name))


class c(ob):
    def __init__(self, x, y):
        self.a = x
        self.b = y

    @property
    def is_pure_lindy_trace(self):
        return self.a.is_pure_lindy_trace and self.b.is_pure_lindy_trace

    def ap(self, x):
        if c(self, x).is_pure_lindy_trace:
            return c(self, x)
        return ev(self, x, self)

    def ev(self, p, x):
        if self.a == C and is_pair(self.b):
            return c(ev(p, x, self.b.a), ev(p, x, self.b.b))
        if self.a == D and is_pair(self.b):
            if ev(p, x, self.b.a) == ev(p, x, self.b.b):
                return A
            else:
                return B
        if self.a == EV:
            return ev(p, x, ev(p, x, self.b))
        return ap(ev(p, x, self.a), ev(p, x, self.b))

    def __setstate__(self, state):
        self.a, self.b = state

    def __getstate__(self):
        return (self.a.__getstate__(), self.b.__getstate__())

    def __str__(self):
        return "({} :: {})".format(str(self.a), str(self.b))

    def __repr__(self):
        return "c({}, {})".format(repr(self.a), repr(self.b))


class e(ob):
    def __init__(self, x):
        self.a = x
        self.b = self

    def ap(self, x):
        return self.a

    def ev(self, p, x):
        return self.a

    def __setstate__(self, state):
        self.a, = state

    def __getstate__(self):
        return (self.a.__getstate__(),)

    def __str__(self):
        if is_individual(self):
            return "`{}".format(str(self.a))
        return "`({})".format(str(self.a))

    def __repr__(self):
        return "e({})".format(repr(self.a))


class L(ob):
    def __init__(self, name):
        self.name = name
        self.a = self
        self.b = self

    @property
    def is_lindy(self):
        return True

    @property
    def is_pure_lindy_trace(self):
        return True

    def ap(self, x):
        if x.is_pure_lindy_trace:
            return c(self, x)
        return c(self, e(x))

    def __setstate__(self, state):
        self.name = state

    def __getstate__(self):
        return self.name

    def __str__(self):
        return '{}'.format(str(self.name))

    def __repr__(self):
        return "L({})".format(repr(self.name))


class Individual(ob):
    def __init__(self, name):
        self.name = name
        self.a = self
        self.b = self

    def __setstate__(self, state):
        self.name = state

    def __getstate__(self):
        return self.name

    def __str__(self):
        return ".{}".format(self.name)

    def __repr__(self):
        return self.name


class NIL_(Individual):
    def ap(self, x):
        return x


class A_(Individual):
    def ap(self, x):
        return a(x)


class B_(Individual):
    def ap(self, x):
        return b(x)


class C_(Individual):
    def ap(self, x):
        return c(C, c(e(x), ARG))


class D_(Individual):
    def ap(self, x):
        return c(D, c(e(x), ARG))


class E_(Individual):
    def ap(self, x):
        return e(x)


class SELF_(Individual):
    def ev(self, p, x):
        return p


class ARG_(Individual):
    def ev(self, p, x):
        return x


class EV_(Individual):
    pass


NIL = NIL_('NIL')
A = A_('A')
B = B_('B')
C = C_('C')
D = D_('D')
E = E_('E')
SELF = SELF_('SELF')
ARG = ARG_('ARG')
EV = EV_('EV')


def a(z): return z.a


def b(z): return z.b


def is_singleton(x): return b(x) == x


def is_individual(x): return a(x) == x


def is_pair(x): return isinstance(x, c)


def is_lindy(x): return getattr(x, 'is_lindy', False) and x.is_lindy


def ap(p, x):
    res = p.ap(x)
    if DEBUG:
        print("ap ({}) ({}) -> {}".format(p, x, res))
    return res


def ev(p, x, exp):
    res = exp.ev(p, x)
    if DEBUG:
        print("ev ({}) ({}) ({}) -> {}".format(p, x, exp, res))
    return res


def eval(exp):
    return ev(SELF, ARG, exp)


namespace = {('.' + k): v for k, v in vars().items() if isinstance(v, ob)}
namespace.update({'L(': L, 'e(': e, 'c(': c, 'ap(': ap})


def test():
    x = L("x")
    l = L("ImLindy")
    EXAMPLE = e(
        c(c(x, l), e(NIL))
    )

    print(EXAMPLE)
    print(repr(EXAMPLE))
    print(eval(EXAMPLE))
    print(NIL, repr(NIL))
    print(EV, repr(EV))

    print(eval(c(c(L("X"), L("Z")), c(L("Y"), L("Z")))))

    exp = (e(cK) ** e(L("X"))) ** e(L("Y"))
    print("{} == {}".format(exp, eval(exp)))
    assert eval(exp) == L("X")


if __name__ == "__main__":
    test()
