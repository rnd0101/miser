class Ob(object):
    a = None
    b = None
    type_ = 'ob'

    def __init__(self, name):
        self.name = name

    def is_enclosure(self):
        return False

    def is_pair(self):
        return False

    def is_individual(self):
        return self.a == self.b

    def is_primitive(self):
        return False

    def is_lindy(self):
        return False

    def is_pure_lindy(self):
        return self.is_lindy()

    def is_lindy_everywhere(self):
        return self.is_lindy()

    def is_singleton(self):
        return ob.b(self) == self

    def obap_ap(self, x):
        return obap.apint(self, x)

    def obap_int(self, x):
        raise ValueError("Ob individual {} can't be interpreted.".format(repr(self)))

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Ob({})".format(repr(self.name))


class Individual(Ob):
    type_ = 'individual'

    def __init__(self, name):
        self.a = self
        self.b = self
        self.name = name

    def is_individual(self):
        return True

    def __eq__(self, other):
        return self is other


class Enclosure(Ob):
    type_ = 'enclosure'

    def __init__(self, x):
        self.a = x
        self.b = self

    def is_enclosure(self):
        return True

    def is_pure_lindy(self):
        return False

    def is_lindy_everywhere(self):
        return self.a.is_lindy_everywhere()

    def obap_ap(self, x):
        return ob.a(x)

    def __eq__(self, other):
        return self.a == other.a

    def __str__(self):
        return "`({})".format(str(self.a))

    def __repr__(self):
        return "ob.e({})".format(repr(self.a))


class Pair(Ob):
    type_ = 'pair'

    def __init__(self, x, y):
        self.a = x
        self.b = y

    def is_pair(self):
        return True

    def is_pure_lindy(self):
        return self.a.is_pure_lindy() and self.b.is_pure_lindy()

    def is_lindy_everywhere(self):
        return self.a.is_lindy_everywhere() and self.b.is_lindy_everywhere()

    def obap_ap(self, x):
        if self.is_pure_lindy() and x.is_lindy_everywhere:
            return ob.c(self, x)
        else:
            return obap.ev(self, x, self)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __str__(self):
        return "({} :: {})".format(str(self.a), str(self.b))

    def __repr__(self):
        return "ob.c({}, {})".format(repr(self.a), repr(self.b))


class Primitive(Individual):
    type_ = 'primitive'

    def __init__(self, name, apint):
        self.a = self
        self.b = self
        self.name = name
        self.apint = apint

    def obap_int(self, x):
        return self.apint(self, x)

    def is_primitive(self):
        return True

    def __eq__(self, other):
        return self.name == other.name and self.type_ == other.type_


class Lindy(Individual):
    type_ = 'lindy'

    def is_lindy(self):
        return True

    def __eq__(self, other):
        return self.name == other.name and self.type_ == other.type_

    def __str__(self):
        return '"{}"'.format(str(self.name))

    def __repr__(self):
        return "Lindy({})".format(repr(self.name))


class ob(object):
    NIL = Primitive('NIL', lambda self, x: x)

    @classmethod
    def a(cls, x):
        return x.a

    @classmethod
    def b(cls, x):
        return x.b

    @classmethod
    def c(cls, x, y):
        return Pair(x, y)

    @classmethod
    def e(cls, x):
        return Enclosure(x)


class obap(object):
    ARG = Primitive('ARG', lambda self, x: ob.c(ob.e(self), ob.e(x)))
    SELF = Primitive('SELF', lambda self, x: ob.c(ob.e(self), ob.e(x)))
    EV = Primitive('EV', lambda self, x: ob.c(ob.e(self), ob.e(x)))
    A = Primitive('A', lambda self, x: ob.a(x))
    B = Primitive('B', lambda self, x: ob.b(x))
    C = Primitive('C', lambda self, x: ob.c(self, ob.c(ob.e(x), obap.ARG)))
    D = Primitive('D', lambda self, x: ob.c(self, ob.c(ob.e(x), obap.ARG)))
    E = Primitive('E', lambda self, x: ob.e(x))

    @staticmethod
    def ap(p, x):
        """determines the application of ob p, taken as
           expression of a procedure, to ob x, taken as
           the operand"""
        return p.obap_ap(x)

    @staticmethod
    def apint(p, x):
        return p.obap_int(x)

    @staticmethod
    def d(x, y):
        return obap.A if x == y else obap.B

    @staticmethod
    def ev(p, x, e):
        if e is obap.SELF:
            return p
        if e is obap.ARG:
            return x
        if e.is_individual():
            return e
        if e.is_enclosure():
            return ob.a(e)
        assert e.is_pair()
        e_a = ob.a(e)
        e_b = ob.b(e)
        if e_a == obap.EV:
            return obap.ev(p, x, obap.ev(p, x, e_b))
        if e_a == obap.C:
            if e_b.is_singleton():
                return obap.ap(e_a, obap.ev(p, x, e_b))
            return ob.c(obap.ev(p, x, ob.a(e_b)), obap.ev(p, x, ob.b(e_b)))
        if e_a == obap.D:
            if e_b.is_singleton():
                return obap.ap(e_a, obap.ev(p, x, e_b))
            return obap.d(obap.ev(p, x, ob.a(e_b)), obap.ev(p, x, ob.b(e_b)))
        return obap.ap(obap.ev(p, x, e_a), obap.ev(p, x, e_b))

    @staticmethod
    def eval(e):
        return obap.ev(obap.SELF, obap.ARG, e)


def repl_loop():
    while True:
        s = input("oMiser> ")
        print("INPUT: {}".format(repr(s)))
        print("\nINPUT: {}".format(str(s)))
        print("\nOUTPUT: {}".format(repr(obap.eval(s))))


def test():
    x = Ob('x')
    y = Ob('y')
    l = Lindy('ImLindy')
    assert Lindy('x') != x  # TODO: fix for python3
    assert Lindy('x') != Primitive('x', lambda self, x: x)
    assert ob.c(x, ob.e(y)) == ob.c(x, ob.e(y))

    print(obap.D.obap_int(x))

    EXAMPLE = ob.e(
        ob.c(ob.c(x, l), ob.e(ob.NIL))
    )

    print(EXAMPLE)
    print(repr(EXAMPLE))
    print(obap.eval(EXAMPLE))


if __name__ == '__main__':
    repl_loop()
