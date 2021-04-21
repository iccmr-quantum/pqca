"""Test the Vector class."""

import pytest
import pqca #pylint: disable=import-error


def test_vector_creation():
    """Create and check equality."""
    assert pqca.Vector() == pqca.Vector()
    assert pqca.Vector([1, 2]) == pqca.Vector([1, 2])
    assert pqca.Vector([1, 2]) != pqca.Vector([2, 1])


def test_vector_extension():
    """Test the .extend function."""
    assert pqca.Vector().extend(1) == pqca.Vector([1])
    assert pqca.Vector([2]).extend(1) == pqca.Vector([2, 1])


def test_vector_string():
    """Test str(Vector)."""
    assert str(pqca.Vector([1, 2])) == "Vector[1, 2]"


def test_vector_arithmetic():
    """Test addition and subtraction."""
    assert pqca.Vector([1, 1]) + pqca.Vector([2, 3]) == pqca.Vector([3, 4])
    assert pqca.Vector([1, 1]) - pqca.Vector([2, 3]) == pqca.Vector([-1, -2])
