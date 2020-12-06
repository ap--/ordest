# ordest

```
from ordest import OrderedSet
>>> "".join(OrderedSet("orderedset"))
"ordest"
```

This will be a playground to implement the "best" :heart: ordered set for 
Python :snake:.
The initial implementation already passes a very large portion of the cpython
test suite for sets, and it remembers insertion order.
I believe that everyone implements their own `OrderedSet` because it's actually
quite easy to get something that works for your specific use case and it's a
nice and small little project. I've seen no benchmarks though.

### Goals

So the immediate term goals of this projects are:

- implement a complete test suite for drop-in replacement testing and all weird
  ordered set flavors that might be nice to have
- benchmark all these ordered set implementations against real world use cases
  and clearly document the results and allow everyone to reproduce them

There will be quite a few implementation related things to consider, that will 
all be fun to think about:

#### Some examples, regarding drop-in replacement support:

- Python's builtin `set` doesn't support many operators directly with other
  iterables, i.e.:
  ```pycon
  >>> set() & [1,2,3]
  Traceback (most recent call last):
    File "<input>", line 1, in <module>
  TypeError: unsupported operand type(s) for &: 'set' and 'list'
  ```
- the builtin `set` automatically casts values of type `set` to `frozenset` in
  `__contains__`, `remove` and `discard`. This is probably a leftover from 
  the Python `sets.Set` implementation which supported an `__as_immutable__`
  Protocol. Note the difference in `set` and `dict`:
  ```pycon
  >>> {1,2} in set()
  False
  >>> {1,2} in {}
  Traceback (most recent call last):
    File "<input>", line 1, in <module>
  TypeError: unhashable type: 'set'
  ```
- `set` reuses calculated hashes as much as possible, which is as far as I
  know currently, impossible to implement in functionality implemented in pure 
  Python that has to iterate in Python land.
- `set` still supports a legacy `__getitem__` only iterator interface, which
  might add some overhead in a custom implementation...
  

#### Something else to consider is behavior when doing comparisons:

- what is equality for and ordered set?
  ```python
  # Are these True or False?
  OrderedSet([1,2,3]) == OrderedSet([3,2,1])
  OrderedSet([1,2,3]) == {1, 2, 3}
  OrderedSet([1,2,3]) == [1, 2, 3]
  ```
- when is an ordered set a subset?
  ```python
  # Are these True or False?
  OrderedSet([1,2,3]).issubset(OrderedSet([1,2,3,4]))
  OrderedSet([3,2,1]).issubset(OrderedSet([1,2,3,4]))
  OrderedSet([1,3]).issubset(OrderedSet([1,2,3,4]))
  OrderedSet([1,3]).issubset({1,2,3,4})
  OrderedSet([1,3]).issubset([1,2,3,4])
  ```


#### And of course some stuff regarding operations:

- Should operations with unordered containers be allowed?
  ```python
  OrderedSet() & {1,2,3}  # should this raise a TypeError?
  ```


Ultimately it'll be fun to implement this in C. Let's see first how fast we can
push this in pure Python.


### Other implementations

I'll collect all implementations of ordered sets here for now. Ultimately I'd
like to document the differences between them and benchmark all operations
for each of them.

- [OrderedSet](https://code.activestate.com/recipes/576694-orderedset/) Recipe
  from Raymond Hettinger posted on activestate
- [OrderedSet with weakrefs](https://code.activestate.com/recipes/576696/) 
  Recipe from Raymond Hettinger similar to above but using weakrefs in the
  internal linked list to prevent circular reference issues
- [orderedset](https://pypi.org/project/orderedset/) cython implementation
  of an ordered set. Supposedly fast, but no obvious benchmark results shown.
  Allows comparison with unordered sets but not equality.
- [ordered-set](https://github.com/LuminosoInsight/ordered-set) an
  implementation based on Raymond Hettingers OrderedSet with some extra support
  for numpy like indexing
- [ubelt.orderedset](https://github.com/Erotemic/ubelt/blob/master/ubelt/orderedset.py)
  ordered set implementation based on the recipe but combining with Sequence
  and some compatibility with numpy and pandas
- [ordered-set-37](https://github.com/bustawin/ordered-set-37) an 
  implementation similar to this one, based on guaranteed to be ordered dicts
  in python37+
- [ordered-hash-set](https://github.com/buyalsky/ordered-hash-set) ordered
  set based on internal dict with indexing support
- [sqlalchemy.util](https://github.com/sqlalchemy/sqlalchemy/blob/master/lib/sqlalchemy/util/_collections.py)
  ordered set keeping a list for ordering in sync
- [sortedcollections](http://www.grantjenks.com/docs/sortedcollections/_modules/sortedcollections/recipes.html#OrderedSet)
  another minimal set/sequence implementation
- [nr.collections](https://git.niklasrosenstein.com/NiklasRosenstein/nr/src/branch/develop/nr.collections)
  uses a collections.deque internally to support popleft

### Contributing

If you find more implementations please share :smiley: :heart:
Shoot me a message if there's anything you want to talk about!
And feel of course free to open as many issues and PR in here as you like!

Cheers,
Andreas :smiley:
