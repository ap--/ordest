"""This module implements an insertion order preserving set container, OrderedSet.

* OrderedSet   mutable set container that preserves insertion order

"""

__all__ = ["OrderedSet"]
__author__ = "Andreas Poehlmann"
__email__ = "andreas@poehlmann.io"

from collections.abc import MutableSet as _MutableSet

try:
    from ordest._version import version as __version__
except ImportError:
    __version__ = "not-installed"


class OrderedSet(_MutableSet):
    """OrderedSet() -> new empty OrderedSet object
    OrderedSet(iterable) -> new OrderedSet object

    Build an insertion order preserving collection of unique elements.
    """

    __slots__ = ("__map",)

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
