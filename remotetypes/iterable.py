import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import Ice
from typing import Optional

class Iterable(rt.Iterable):
    """Base class for Iterable implementations."""

    def __init__(self, collection):
        self.collection = collection
        self.iterator = iter(collection)
        self.modified = False

    def next(self, current: Optional[Ice.Current] = None):
        """Return the next element in the iteration."""
        if self.modified:
            raise rt.CancelIteration("The collection has been modified")
        try:
            return next(self.iterator)
        except StopIteration:
            raise rt.StopIteration("End of iteration")

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Return an iterable proxy."""
        adapter = current.adapter
        proxy = adapter.addWithUUID(self)
        return rt.IterablePrx.uncheckedCast(proxy)


class SetIterable(Iterable):
    """Iterable implementation for sets."""

    def __init__(self, collection):
        super().__init__(collection)
        self.original_hash = hash(frozenset(collection))

    def next(self, current: Optional[Ice.Current] = None):
        """Return the next element in the iteration."""
        if self.original_hash != hash(frozenset(self.collection)):
            self.modified = True
        return super().next(current)

class DictIterable(Iterable):
    """Iterable implementation for dictionaries."""

    def __init__(self, collection):
        super().__init__(collection.items())
        self.original_hash = hash(frozenset(collection.items()))

    def next(self, current: Optional[Ice.Current] = None):
        """Return the next element in the iteration."""
        if self.original_hash != hash(frozenset(self.collection.items())):
            self.modified = True
        return super().next(current)

class ListIterable(Iterable):
    """Iterable implementation for lists."""

    def __init__(self, collection):
        super().__init__(collection)
        self.original_hash = hash(tuple(collection))

    def next(self, current: Optional[Ice.Current] = None):
        """Return the next element in the iteration."""
        if self.original_hash != hash(tuple(self.collection)):
            self.modified = True
        return super().next(current)
