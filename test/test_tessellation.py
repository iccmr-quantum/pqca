"""Test tessellation of circuits."""

# pylint: disable=import-error
import itertools
import re
import pytest
import pqca


def test_create_one_dimensional():
    """Tessellate a (finite) line."""
    tes_one = pqca.tessellation.one_dimensional(10, 2)
    assert str(
        tes_one) == "Tessellation(10 qubits as 5 cells, first cell: [0, 1])"


def test_when_n_is_one():
    """Check that one_dimensional and n_dimensional overlap when n=1."""
    tes_one = pqca.tessellation.one_dimensional(10, 2)
    tes_n = pqca.tessellation.n_dimensional([10], [2])
    assert tes_one.cells == tes_n.cells


def test_vector_to_name():
    """Convert a vector to a point in lexicographic order."""
    Vector = pqca.Vector
    vtn = pqca.tessellation.vector_to_name
    assert vtn(Vector([5]), [6]) == 5
    assert vtn(Vector([5, 0]), [6, 6]) == 5*6
    assert vtn(Vector([0, 0]), [6, 6]) == 0
    assert vtn(Vector([0, 5]), [6, 6]) == 5
    assert vtn(Vector([1, 5]), [6, 6]) == 6+5
    assert vtn(Vector([1, 2]), [6, 3]) == 1*3+2
    assert vtn(Vector([0, 2, 0]), [6, 5, 4]) == 2*4
    assert vtn(Vector([1, 2, 3]), [6, 5, 4]) == 1*5*4 + 2*4+3


def test_cell_of_given_size():
    """Test creation of the first cell."""
    cell = pqca.tessellation.cell_of_given_size([2, 3, 2])
    print(cell)
    assert len(cell) == 2*3*2
    assert pqca.Vector([0, 0, 0]) in cell
    assert pqca.Vector([1, 2, 1]) in cell


def test_invalid_n_dimensional():
    """Passing impossible arguments to the creator should fail informatively."""
    with pytest.raises(AssertionError):
        pqca.tessellation.n_dimensional([4, 4], [2, 3])


def test_create_n_dimensional():
    """Tessellate a (finite) lattice."""
    for dimension in (1, 2, 3, 4):
        total_qubits = pow(6, dimension)
        total_cells = pow(3, dimension)
        tes = pqca.tessellation.n_dimensional([6]*dimension, [2]*dimension)
        assert re.match(f"Tessellation\\({total_qubits} qubits as" +
                        f" {total_cells} cells", str(tes)) is not None
