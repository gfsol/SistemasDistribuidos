"""Needed classes to implement and serve the RList type."""
import json
from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.iterable import Iterable  # Importar la clase Iterable

class RemoteList(rt.RList):
    """Implementation of the remote interface RList."""

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Initialise a RemoteList with an empty list or load from file."""
        self.storage = []
        self.identifier = identifier
        self.file_path = f"{self.identifier}.json" if identifier else None
        if identifier:
            self._load_from_file()

    def _load_from_file(self) -> None:
        """Load the list from a JSON file."""
        if self.file_path:
            try:
                with open(self.file_path, "r") as file:
                    self.storage = json.load(file)
            except FileNotFoundError:
                pass

    def _save_to_file(self) -> None:
        """Save the list to a JSON file."""
        if self.file_path:
            with open(self.file_path, "w") as file:
                json.dump(self.storage, file)

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add an element to the end of the list."""
        self.storage.append(item)
        self._save_to_file()

    def pop(self, index: Optional[int] = Ice.Unset, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the list."""
        if index is Ice.Unset:
            item = self.storage.pop()
        else:
            item = self.storage.pop(index)
        self._save_to_file()
        return item

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Get an element from a specific position in the list."""
        if index < len(self.storage):
            return self.storage[index]
        else:
            raise IndexError("Index out of range")

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the list."""
        self.storage.remove(item)
        self._save_to_file()

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the list."""
        return len(self.storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the list contains an item."""
        return item in self.storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the list."""
        return hash(tuple(self.storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        iterable = Iterable(self.storage)
        adapter = current.adapter
        proxy = adapter.addWithUUID(iterable)
        return rt.IterablePrx.uncheckedCast(proxy)

