"""Module docstring: This module contains iterable implementations for various collection types."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import Ice
from typing import Optional

class Iterable(rt.Iterable):
    """Base class for Iterable implementations."""

    def __init__(self, collection):
        """Initialize the Iterable with a collection.

        Args:
            collection (iterable): The collection to be iterated over.

        """
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
        """Initialize the SetIterable with a set collection.

        Args:
            collection (set): The set collection to be iterated over.

        """
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
        """Initialize the DictIterable with a dictionary collection.

        Args:
            collection (dict): The dictionary collection to be iterated over.

        """
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
        """Initialize the ListIterable with a list collection.

        Args:
            collection (list): The list collection to be iterated over.

        """
        super().__init__(collection)
        self.original_hash = hash(tuple(collection))

    def next(self, current: Optional[Ice.Current] = None):
        """Return the next element in the iteration."""
        if self.original_hash != hash(tuple(self.collection)):
            self.modified = True
        return super().next(current)
