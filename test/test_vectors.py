"""Test the Vector class."""

# pylint: disable=import-error
import pytest
import pqca
from pqca.vector import Vector


def test_vector_creation():
    """Create and check equality."""
    assert Vector() == Vector()
    assert Vector([1, 2]) == Vector([1, 2])
    assert Vector([1, 2]) != Vector([2, 1])


def test_entry_access():
    """Test the __getitem___."""
    assert Vector([1, 2])[0] == 1


def test_vector_extension():
    """Test the .extend function."""
    assert Vector().extend(1) == Vector([1])
    assert Vector([2]).extend(1) == Vector([2, 1])


def test_vector_string():
    """Test str(Vector)."""
    assert str(Vector([1, 2])) == "Vector[1, 2]"


def test_vector_arithmetic():
    """Test addition and subtraction."""
    assert Vector([1, 1]) + Vector([2, 3]) == Vector([3, 4])
    assert Vector([1, 1]) - Vector([2, 3]) == Vector([-1, -2])
