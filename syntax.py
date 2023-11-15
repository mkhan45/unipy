import uni

class Var:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return Equal(self, other)

    def reify(self, _):
        return ('var', self.name)

    def weird_ast(self): return reify(self)

class Equal:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + ' = ' + str(self.b)

    def reify(self, s=[]):
        return uni.eq(reify(self.a), reify(self.b), s)

    def weird_ast(self): return ('eq', weird_ast(self.a), weird_ast(self.b))

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

    def weird_ast(self): return [weird_ast(self.a), weird_ast(self.b)]

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

def weird_ast(q):
    if isinstance(q, int): return ('num', q)
    if isinstance(q, tuple):
        nt = ()
        for t in q: nt += (weird_ast(t),)
        return nt
    else: return q.weird_ast()

def real_run(q, s=[]):
    res = uni.unify_in(weird_ast(q), s)
    return Substs(res)

class RelationCall:
    def __init__(self, rel, args):
        self.rel = rel
        self.args = args

    def __and__(self, other):
        return And(self, other)

    def __str__(self):
        return self.rel.name + '(' + ', '.join(map(str, self.args)) + ')'

    def __repr__(self):
        return str(self)

    def weird_ast(self):
        return ('rel_app', weird_ast(self.rel), [weird_ast(a) for a in self.args])

class Relation:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __call__(self, *args):
        assert(len(args) == len(self.args))
        return RelationCall(self, args)

    def weird_ast(self): 
        return ('rel', self.name, self.args, [weird_ast(b) for b in self.body])

    def __str__(self):
        body_str = ', '.join(str(Equal(l, r)) for (l, r) in self.body)
        return self.name + '(' + ', '.join(map(str, self.args)) + ')' + ' :- ' + body_str
    
    def __repr__(self):
        return str(self)

def tests():
    def test1():
        x = Var('x')
        y = Var('y')
        t = (x == 1) & (x == y)
        res = run(t)
        print(f"[ {t} ]\n\t==> [ {res} ]")
        assert(res['x'] == 1)
        assert(res['y'] == 1)

    def test2():
        x = Var('x')
        y = Var('y')

        eq1 = Relation('eq1', ['x'], [(x, 1)])
        t = eq1(x) & (x == y)
        res = real_run(t)
        print(eq1)
        print(f"[ {t} ]\n\t==> [ {res} ]")
        # assert(res['x'] == 1)
        # assert(res['y'] == 1)

    test1()
    test2()

tests()
