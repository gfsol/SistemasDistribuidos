import json
from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import os
from remotetypes.iterable import Iterable  # Importar la clase Iterable

class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Initialise a RemoteSet with an empty set or load from file."""
        self.storage = set()
        self.identifier = identifier
        self.file_path = f"{self.identifier}.json" if identifier else None
        if identifier:
            self._load_from_file()

    def _load_from_file(self) -> None:
        """Load the set from a JSON file."""
        if self.file_path:
            try:
                with open(self.file_path, "r") as file:
                    self.storage = set(json.load(file))
            except FileNotFoundError:
                pass

    def _save_to_file(self) -> None:
        """Save the set to a JSON file."""
        if self.file_path:
            with open(self.file_path, "w") as file:
                json.dump(list(self.storage), file)

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add an element to the set."""
        self.storage.add(item)
        self._save_to_file()

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the set."""
        self.storage.remove(item)
        self._save_to_file()

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the set contains an item."""
        return item in self.storage

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the set."""
        return len(self.storage)

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the set."""
        return hash(frozenset(self.storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        iterable = Iterable(list(self.storage))
        adapter = current.adapter
        proxy = adapter.addWithUUID(iterable)
        return rt.IterablePrx.uncheckedCast(proxy)