"""Needed classes to implement and serve the RDict type."""

import json
from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import os
from remotetypes.iterable import Iterable  # Importar la clase Iterable

class RemoteDict(rt.RDict):
    """Implementation of the remote interface RDict."""

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Initialise a RemoteDict with an empty dict or load from file."""
        self.storage = {}
        self.identifier = identifier
        self.file_path = f"{self.identifier}.json" if identifier else None
        if identifier:
            self._load_from_file()

    def _load_from_file(self) -> None:
        """Load the dict from a JSON file."""
        if self.file_path:
            try:
                with open(self.file_path, "r") as file:
                    self.storage = json.load(file)
            except FileNotFoundError:
                pass

    def _save_to_file(self) -> None:
        """Save the dict to a JSON file."""
        if self.file_path:
            with open(self.file_path, "w") as file:
                json.dump(self.storage, file)

    def setItem(self, key: str, value: str, current: Optional[Ice.Current] = None) -> None:
        """Set an item in the dict."""
        self.storage[key] = value
        self._save_to_file()

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Get an item from the dict."""
        try:
            return self.storage[key]
        except KeyError:
            raise KeyError("Key not found")

    def remove(self, key: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the dict."""
        try:
            del self.storage[key]
            self._save_to_file()
        except KeyError:
            raise KeyError("Key not found")

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an item from the dict."""
        try:
            value = self.storage.pop(key)
            self._save_to_file()
            return value
        except KeyError:
            raise KeyError("Key not found")

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the dict."""
        return len(self.storage)

    def contains(self, key: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the dict contains a key."""
        return key in self.storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the dict."""
        return hash(frozenset(self.storage.items()))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        iterable = Iterable(list(self.storage.items()))
        adapter = current.adapter
        proxy = adapter.addWithUUID(iterable)
        return rt.IterablePrx.uncheckedCast(proxy)
