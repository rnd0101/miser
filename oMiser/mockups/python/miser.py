class Ob(object):
    a = None
    b = None

    def __init__(self, name):
        self.name = name

    def is_enclosure(self):
        return False

    def is_pair(self):
        return False

    def is_individual(self):
        return False

    def is_primitive(self):
        return False

    def is_lindy(self):
        return False

    def is_singleton(self):
        return ob.b(self) == self

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Ob({})".format(repr(self.name))


class Individual(Ob):
    def __init__(self, name):
        self.a = self
        self.b = self
        self.name = name

    def is_individual(self):
        return True

    def __eq__(self, other):
        return self is other


class Enclosure(Ob):
    def __init__(self, x):
        self.a = x
        self.b = self

    def is_enclosure(self):
        return True

    def __eq__(self, other):
        return self.a == other.a

    def __str__(self):
        return "`({})".format(str(self.a))

    def __repr__(self):
        return "ob.e({})".format(repr(self.a))


class Pair(Ob):
    def __init__(self, x, y):
        self.a = x
        self.b = y

    def is_pair(self):
        return False

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __str__(self):
        return "({} :: {})".format(str(self.a), str(self.b))

    def __repr__(self):
        return "ob.c({}, {})".format(repr(self.a), repr(self.b))


class Primitive(Individual):
    def is_primitive(self):
        return True


class Lindy(Individual):
    def is_lindy(self):
        return True

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return '"{}"'.format(str(self.name))

    def __repr__(self):
        return "Lindy({})".format(repr(self.name))


class ob(object):
    NIL = Primitive('NIL')

    @classmethod
    def a(self, x):
        return x.a

    @classmethod
    def b(self, x):
        return x.b

    @classmethod
    def c(self, x, y):
        return Pair(x, y)

    @classmethod
    def e(self, x):
        return Enclosure(x)


class obap(object):
    A = Primitive('A')
    B = Primitive('B')
    C = Primitive('C')
    D = Primitive('D')
    E = Primitive('E')
    SELF = Primitive('SELF')
    ARG = Primitive('ARG')
    EV = Primitive('EV')


x = Ob('x')
y = Ob('y')
l = Lindy('ImLindy')

EXAMPLE = ob.e(
    ob.c(ob.c(x, l), ob.e(ob.NIL))
)

print(EXAMPLE)
print(repr(EXAMPLE))
