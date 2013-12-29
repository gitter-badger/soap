import copy
from contextlib import contextmanager

from soap.common.cache import invalidate_cache


class RestoreSnapshotError(Exception):
    """Cannot restore snapshot.  """


class _ContextDict(dict):
    """
    _ContextDict, a dictionary subclass with dot syntax and snapshot support.
    """
    def __init__(self, dictionary=None, **kwargs):
        if dictionary:
            kwargs.update(dictionary)
        kwargs = {k: self._cast_dict(v) for k, v in kwargs.items()}
        with self.no_invalidate_cache():
            super().__init__(kwargs)

    @contextmanager
    def no_invalidate_cache(self):
        self.should_invalidate_cache = False
        yield
        del self.should_invalidate_cache

    def __setattr__(self, key, value):
        self[key] = self._cast_dict(value)
        if self.get('should_invalidate_cache', True):
            invalidate_cache()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(str(e))

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(str(e))

    def _cast_dict(self, dictionary):
        if not isinstance(dictionary, dict):
            return dictionary
        dictionary = {k: self._cast_dict(v) for k, v in dictionary.items()}
        return self.__class__(dictionary)

    def take_snapshot(self):
        self.__snapshot__ = copy.deepcopy(self)

    def restore_snapshot(self):
        if '__snapshot__' not in self:
            raise RestoreSnapshotError(
                'Cannot restore snapshot: no snapshot exists.')
        snapshot = self.__snapshot__
        self.update(snapshot)
        for k in list(self.keys()):
            if k not in snapshot:
                del self[k]

    @contextmanager
    def local(self, dictionary=None, **kwargs):
        """Withable local context.  """
        self.take_snapshot()
        self.update(dict(dictionary or {}, **kwargs))
        yield
        self.restore_snapshot()
