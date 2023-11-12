import uni

class Var:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return Equal(self, other)

    def reify(self, _):
        return ('var', self.name)

class Equal:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + ' = ' + str(self.b)

    def reify(self, s=[]):
        return uni.eq(reify(self.a), reify(self.b), s)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        lhs = uni.eq(self.a, self.b)
        rhs = uni.eq(other.a, other.b)
        return uni.or_(lhs, rhs)

class And:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + ' & ' + str(self.b)

    def reify(self, s=[]):
        s1 = reify(self.a, s)
        s2 = reify(self.b, s1)
        return s2

    def __and__(self, other): return And(self, other)
    def __or__(self, other): return Or(self, other)

class Or:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + ' | ' + str(self.b)

    def reify(self, s=[]):
        return uni.or_(reify(self.a), reify(self.b), s)

    def __and__(self, other): return And(self, other)
    def __or__(self, other): return Or(self, other)

class Substs:
    def __init__(self, s=[]):
        self.s = s

    def aux(v):
        match v:
            case ('var', x): return x
            case ('num', n): return n
            case _: return v

    def __str__(self):
        print(self.s)
        return ', '.join(f"{k} = {Substs.aux(v)}" for (k, v) in self.s)

    def __getitem__(self, key):
        for (k, v) in self.s:
            if k == key: return Substs.aux(v)
        return None

def reify(x, s=[]):
    if isinstance(x, int): return ('num', x)
    else: return x.reify(s)

def run(q, s=[]):
    return Substs(reify(q, s))

class Relation:
    def __init__(self, name, *args, body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return self.name + '(' + ', '.join(map(str, self.args)) + ')' + ' :- ' + str(self.body)

x = Var('x')
y = Var('y')
t = (x == 1) & (x == y)
res = run(t)
print(res) # x = 1, y = 1
