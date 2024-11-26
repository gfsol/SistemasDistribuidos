"""Implementation of custom sets."""

from typing import Optional


class StringSet(set):
    """Set that only allows adding str objects."""

    def __init__(
        self,
        *args: tuple[object],
        force_upper_case: Optional[bool] = False,
        **kwargs: dict[str, object],
    ) -> None:
        """Build an unordered collection of unique elements of type str.

        StringSet() -> new empty StringSet object
        StringSet(iterable) -> new StringSet object
        """
        self.upper_case = force_upper_case
        for arg in args:
            if isinstance(arg, (list, set, tuple)):
                for item in arg:
                    if not isinstance(item, str):
                        raise ValueError(f"All elements must be of type str, but got {type(item).__name__}")
            elif not isinstance(arg, str):
                raise ValueError(f"All elements must be of type str, but got {type(arg).__name__}")
        super().__init__(*args, **kwargs)

    def add(self, item: str) -> None:
        """Add an element to a set. Checks the element type to be a str."""
        if not isinstance(item, str):
            raise ValueError(item)

        if self.upper_case:
            item = item.upper()

        return super().add(item)

    def __contains__(self, o: object) -> bool:
        """Overwrite the `in` operator.

        x.__contains__(y) <==> y in x.
        """
        if not isinstance(o, str):
            o = str(o)

        if self.upper_case:
            o = o.upper()

        return super().__contains__(o)
