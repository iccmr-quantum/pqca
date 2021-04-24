"""Simple n-dimensional, extendable vector of ints."""

from __future__ import annotations
from typing import Callable, List, Tuple


class Vector:
    """Wrap a list of entries with helper functions."""

    entries: List[int]

    def __init__(self, entries: List[int] = None):
        """Convert a tuple of ints into coordinates."""
        self.entries = entries if entries is not None else []

    def extend(self, next_entry: int):
        """Add the given entry to the end of the list of entries."""
        return Vector(list(self.entries) + [next_entry])

    def action(self, other: Vector, action: Callable[[int, int], int]):
        """Apply the action to two vectors."""
        return Vector([action(a, b) for (a, b) in zip(self.entries, other.entries)])

    def __add__(self, other: Vector):
        """Add two vectors."""
        return self.action(other, lambda x, y: x+y)

    def __sub__(self, other: Vector):
        """Subtract two vectors."""
        return self.action(other, lambda x, y: x-y)

    def __eq__(self, other: Vector):
        """Compare component-wise."""
        return self.entries == other.entries

    def __getitem__(self, item):
        """Access to entries."""
        return self.entries[item]

    def __str__(self):
        """Human-readable string representation."""
        return f"Vector{self.entries}"

    def __repr__(self):
        """Unambiguous string representation."""
        return str(self)
