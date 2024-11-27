"""Module docstring: This module contains iterable implementations for various collection types."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

class Iterable(rt.Iterable):
    """Skeleton for an Iterable implementation."""

    def __init__(self, collection):
        """Initialize the iterable instance with the collection to iterate over."""
        self.collection = collection
        self.index = 0
        self.initial_state = self._get_state()

    def _get_state(self):
        """Get the current state of the collection."""
        if isinstance(self.collection, (list, set)):
            return hash(tuple(self.collection))
        elif isinstance(self.collection, dict):
            return hash(frozenset(self.collection.items()))
        else:
            raise TypeError("Unsupported collection type")

    def next(self, current=None):
        """Return the next item in the collection."""
        if self._get_state() != self.initial_state:
            raise rt.CancelIteration()

        if self.index >= len(self.collection):
            raise rt.StopIteration()

        item = self.collection[self.index]
        self.index += 1
        return item
