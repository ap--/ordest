"""This module implements an insertion order preserving set container.

* OrderedSet   mutable set container that preserves insertion order

"""

__all__ = ["OrderedSet"]
__author__ = "Andreas Poehlmann"
__email__ = "andreas@poehlmann.io"

from collections.abc import Iterable as _Iterable
from collections.abc import MutableSet as _MutableSet
from reprlib import recursive_repr as _recursive_repr

try:
    from ordest._version import version as __version__
except ImportError:
    __version__ = "not-installed"


class OrderedSet(_MutableSet):
    """OrderedSet() -> new empty OrderedSet object
    OrderedSet(iterable) -> new OrderedSet object

    Build an insertion order preserving collection of unique elements.
    """

    def __init__(self, iterable=()):
        self.__map = dict.fromkeys(iterable)

    def __contains__(self, x):
        return x in self.__map

    def __len__(self):
        return len(self.__map)

    def __iter__(self):
        return iter(self.__map)

    def isdisjoint(self, s):
        return self.__map.keys().isdisjoint(s)

    def __le__(self, other):
        return self.__map.keys() <= other

    def __ge__(self, other):
        return self.__map.keys() >= other

    def __eq__(self, other):
        return self.__map.keys() == other

    def __reversed__(self):
        return reversed(self.__map)

    @_recursive_repr()
    def __repr__(self):
        return f"{type(self).__name__}({list(self)!r})"

    # -- MutableSet methods -------------------------------------------

    def add(self, x):
        self.__map[x] = None

    def discard(self, x):
        try:
            del self.__map[x]
        except KeyError:
            pass

    def remove(self, element):
        del self.__map[element]

    def pop(self):
        value, _ = self.__map.popitem()
        return value

    def clear(self):
        self.__map.clear()

    def __ior__(self, other):
        self.__map.update(dict.fromkeys(other))
        return self

    # -- set methods --------------------------------------------------

    def copy(self):
        return self.__class__(self.__map)

    def union(self, *others):
        oset = self.copy()
        oset.update(*others)
        return oset

    def update(self, *others):
        for other in others:
            self.__ior__(other)

    def intersection(self, *others):
        oset = self.copy()
        oset.intersection_update(*others)
        return oset

    def intersection_update(self, *others):
        for other in others:
            self.__iand__(other)

    def difference(self, *others):
        oset = self.copy()
        oset.difference_update(*others)
        return oset

    def difference_update(self, *others):
        for other in others:
            self.__isub__(other)

    def symmetric_difference(self, other):
        oset = self.__xor__(other)
        if oset is NotImplemented:
            raise TypeError(f"{type(self)}.symmetric_difference cannot use type {type(other)}")
        return oset

    def symmetric_difference_update(self, other):
        self.__ixor__(other)

    def issubset(self, other):
        if not isinstance(other, _MutableSet):
            if not isinstance(other, _Iterable):
                return NotImplemented
            other = self.__class__(other)
        return self <= other

    def issuperset(self, other):
        if not isinstance(other, _MutableSet):
            if not isinstance(other, _Iterable):
                return NotImplemented
            other = self.__class__(other)
        return self >= other
