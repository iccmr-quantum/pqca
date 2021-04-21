"""Test tessellation of circuits."""

import itertools
import pytest
import pqca  # pylint: disable=import-error


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
        total_qubits = pow(4, dimension)
        total_cells = pow(2, dimension)
        first_cell = pqca.tessellation.cell_of_given_size([2]*dimension)
        tes = pqca.tessellation.n_dimensional([4]*dimension, [2]*dimension)
        assert str(tes) == f"Tessellation({total_qubits} qubits as" +\
            f" {total_cells} cells, first cell: {first_cell})"
