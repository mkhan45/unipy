# Unipy

Possibly a MiniKanren but I didn't read the book so I'm not sure

```py
x = Var('x')
y = Var('y')
t = (x == 1) & (x == y)
res = run(t)
assert(res['x'] == 1)
assert(res['y'] == 1)
```

There are also relations and disjunctions but probably buggy. The code is
very cursed so I'll rewrite it in Scala
