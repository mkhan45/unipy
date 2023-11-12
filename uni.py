# term = x # variable
#      | n # number
#      | r(term,*) # relation

# expr = ('var', x)
#      | ('num', n)
#      | ('rel', r, [term, ...])
#      | ('rel_app', r, [term, ...])

def subst(v, _for, t2, _in, t3):
    assert(_for == 'for')
    assert(_in == 'in')

    match t3:
        case ('var', x) if x == v:
            return t2
        case ('var' | 'num', _):
            return t3
        case ('rel', r, vs, ts):
            if any(v == v2 for v2 in vs): return t3

            nts = [
                (subst(v, 'for', t2, 'in', l), subst(v, 'for', t2, 'in', r))
                for (l, r) in ts
            ]
            return ('rel', r, vs, nts)

def subst_all(s, _in, t):
    assert(_in == 'in')

    nt = t
    for (v, t2) in s:
        nt = subst(v, 'for', t2, 'in', nt)

    return nt

def unify(t1, _with, t2, _in, s):
    assert(_with == 'with')
    assert(_in == 'in')

    t1 = subst_all(s, 'in', t1)
    t2 = subst_all(s, 'in', t2)

    if t1 == t2: return s

    match (t1, t2):
        case (('var', x), _): return [(x, t2)] + s
        case (_, ('var', x)): return [(x, t1)] + s

        case (('num', n1), ('num', n2)) if n1 != n2: return None
        case (('num', n1), ('num', n2)) if n1 == n2: return s

        # this would be for uninterpreted functions
        # case (('rel', r1, ts1), ('rel', r2, ts2)) if r1 != r2: return None
        # case (('rel', r1, ts1), ('rel', r2, ts2)) if r1 == r2:
        #     ns = s
        #     for (t1, t2) in zip(ts1, ts2):
        #         ns = unify(t1, 'with', t2, 'in', ns)
        #         if ns == None: return None

        #     return ns

def get_rel_constraints(t):
    assert(t[0] == 'rel_app')
    (_, r, ts) = t
    assert(r[0] == 'rel')
    (_, r, vs, cs) = r

    substs = [(v, t) for (v, t) in zip(vs, ts)]
    return [(subst_all(substs, 'in', l), subst_all(substs, 'in', r)) for (l, r) in cs]

def eq(a, b, st): return unify(a, 'with', b, 'in', st)

def and_(a, b, st):
    (t1, t2) = a
    (t3, t4) = b
    s1 = unify(t1, 'with', t2, 'in', st)
    s2 = unify(t3, 'with', t4, 'in', s1)
    return s2

# idk if this is right
def or_(a, b, st):
    (t1, t2) = a
    (t3, t4) = b
    s1 = unify(t1, 'with', t2, 'in', st)
    if s1 == None: return unify(t3, 'with', t4, 'in', st)
    else: return s1

assert(subst('x', 'for', ('num', 1), 'in', ('var', 'x')) == ('num', 1))
assert(subst('x', 'for', ('num', 1), 'in', ('var', 'y')) == ('var', 'y'))

assert(and_((('var', 'x'), ('num', 1)), (('var', 'x'), ('var', 'y')), []) == [('y', ('num', 1)), ('x', ('num', 1))])

r = ('rel', 'eq1', ['x'], [(('var', 'x'), ('num', 1))])
cs = get_rel_constraints(('rel_app', r, [('var', 'x')]))

res = unify(('var', 'y'), 'with', ('var', 'x'), 'in', cs)
assert(res == [('y', ('var', 'x')), (('var', 'x'), ('num', 1))])
