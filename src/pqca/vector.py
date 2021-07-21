"""Simple, n-dimensional, extendable vector of ints."""

from __future__ import annotations
from typing import Callable, List


class Vector:
    """Wrap a list of int entries with helper functions.
    
    For internal use only.
    """

    entries: List[int]

    def __init__(self, entries: List[int] = None) -> Vector:
        """Convert a list of ints into coordinates."""
        self.entries = entries if entries is not None else []

    def extend(self, next_entry: int) -> Vector:
        """Append the given entry to the end of the list of entries."""
        return Vector(list(self.entries) + [next_entry])

    def action(self, other: Vector, action: Callable[[int, int], int]) -> Vector:
        """Apply the action each successive pair of elements in the two vectors."""
        return Vector([action(a, b) for (a, b) in zip(self.entries, other.entries)])

    def __add__(self, other: Vector) -> Vector:
        """Add two vectors."""
        return self.action(other, lambda x, y: x+y)

    def __sub__(self, other: Vector) -> Vector:
        """Subtract two vectors."""
        return self.action(other, lambda x, y: x-y)

    def __eq__(self, other: Vector) -> bool:
        """Compare vectors component-wise."""
        return self.entries == other.entries

    def __getitem__(self, item) -> int:
        """Access to entries."""
        return self.entries[item]

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Vector{self.entries}"

    def __repr__(self) -> str:
        """Unambiguous string representation."""
        return str(self)


"""
The MIT License (MIT)

Copyright (c) 2021 Hector Miller-Bakewell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
