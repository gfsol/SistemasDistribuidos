"""Needed classes to implement the Factory interface."""

from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.remotelist import RemoteList
from remotetypes.remotedict import RemoteDict
from remotetypes.remoteset import RemoteSet

class Factory(rt.Factory):
    """Implementation of the Factory interface."""

    def __init__(self) -> None:
        """Initialize the Factory with storage for created objects."""
        self.objects = {}

    def get(self, typeName: rt.TypeName, identifier: str = None, current: Optional[Ice.Current] = None) -> rt.RTypePrx:
        """Return an object of the specified type, optionally identified by an identifier."""
        key = (typeName, identifier)
        if identifier and key in self.objects:
            return self.objects[key]

        if typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
        elif typeName == rt.TypeName.RList:
            obj = RemoteList(identifier)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        else:
            raise ValueError(f"Unknown typeName: {typeName}")

        if identifier:
            self.objects[key] = obj

        adapter = current.adapter
        proxy = adapter.addWithUUID(obj)
        return rt.RTypePrx.uncheckedCast(proxy)
