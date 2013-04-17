import inspect
import functools
import weakref
import pickle


class DynamicMethods(object):

    def list_method_names(self, predicate):
        """Find all transform methods within the class that satisfies the
        predicate.

        Returns:
            A list of tuples containing method names.
        """
        methods = [member[0] for member in inspect.getmembers(self,
                   predicate=inspect.isroutine)]
        return [m for m in methods if not m.startswith('_') and
                m != 'list_ms' and predicate(m)]

    def list_methods(self, predicate):
        return [getattr(self, m) for m in self.list_method_names(predicate)]


class Comparable(object):

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return not self.__eq__(other) and not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)


CACHE_CAPACITY = 1000000
_cache_map = dict()


def cached(f):
    def decorated(*args, **kwargs):
        key = pickle.dumps((f.__name__, args, tuple(kwargs.items())))
        v = _cache_map.get(key)
        if v is None:
            v = f(*args, **kwargs)
        if len(_cache_map) < CACHE_CAPACITY:
            _cache_map[key] = v
        return v
    return functools.wraps(f)(decorated)


class Flyweight(object):
    _cache = weakref.WeakValueDictionary()

    def __new__(cls, *args, **kwargs):
        if not args and not kwargs:
            return object.__new__(cls)
        key = pickle.dumps((cls, args, list(kwargs.items())))
        v = cls._cache.get(key, None)
        if v:
            return v
        v = object.__new__(cls)
        cls._cache[key] = v
        return v
