"""Create a tessellation from a list of qubits."""

from __future__ import annotations
from typing import List, Callable, Tuple, Iterable
import itertools
import functools
from . import exceptions
from .vector import Vector


class Tessellation:
    """Describes how to partition the lattice into cells.

    This is a list of lists of qubits that also performs some validation.
    """

    size: int

    def __init__(self, cells: List[int]):
        """Treat a list of cells as a tessellation."""
        if len(cells) == 0:
            raise exceptions.NoCellsException
        if len(cells[0]) == 0:
            raise exceptions.EmptyCellException

        self.cells = cells
        self.size = sum([len(c) for c in cells])

        # check no qubit appears twice
        set_of_qubits = {q for cell in self.cells for q in cell}
        if len(set_of_qubits) != self.size:
            raise exceptions.PartitionUnevenlyCoversQubits(cells)
        # check all cells the same size
        if len({len(cell) for cell in cells}) != 1:
            raise exceptions.IrregularCellSize(cells)

    def shifted_by(self, amount=1):
        """Shift the tessellation along by the specified amount."""
        return self.update_names(lambda x: x+amount)

    def update_names(self,
                     name_update: Callable[[int], int],
                     rename_modulo_size=True) -> Tessellation:
        """Create a new tessellation by renaming every qubit in the old one.

        This renaming will happen modulo the number of qubits unless asked not to.
        """
        if rename_modulo_size:
            def make_address_positive(qubit_name):
                while qubit_name < 0:
                    qubit_name += self.size
                while qubit_name >= self.size:
                    qubit_name -= self.size
                return qubit_name
            return Tessellation([
                [make_address_positive(name_update(c)) for c in cell] for cell in self.cells])
        else:
            return Tessellation([[name_update(c) for c in cell] for cell in self.cells])

    def __str__(self):
        """Human-readable string representation."""
        return f"Tessellation({self.size} qubits as " +\
            f"{len(self.cells)} cells, first cell: {self.cells[0]})"


def one_dimensional(num_qubits: int, cell_size: int) -> Tessellation:
    """Partition a line of length num_qubits into cells of size cell_size."""
    return n_dimensional([num_qubits], [cell_size])


def cell_of_given_size(cell_dimension: List[int]) -> List[Vector]:
    """Given a length in each dimension create a cell."""
    points_in_first_cell = itertools.product(
        *list(map(lambda d: list(range(0, d)), cell_dimension))
    )

    first_cell_as_vectors = map(lambda t: Vector(
        list(t)), list(points_in_first_cell))
    return list(first_cell_as_vectors)


def n_dimensional(qubits_in_each_dimension: List[int],
                  cell_size: List[int]) -> Tessellation:
    """Partition an n-dimensional lattice into n-dimensional cuboids.

    example qubits_in_each_dimension: [5,5,10] for a cuboid of size 5 by 5 by 10
    example cell_size: [5,5,2]

    Note that the size of the cell must divide (for each dimension) the number
    of qubits in the lattice.
    """
    for index, length in enumerate(qubits_in_each_dimension):
        try:
            assert length % cell_size[index] == 0
        except:
            raise exceptions.IrregularCoordinateDimensions(
                qubits_in_each_dimension, cell_size) from None

    focal_points_as_product = itertools.product(
        *[range(0, qubits_in_each_dimension[index], cell_size[index])
          for index, _ in enumerate(qubits_in_each_dimension)]
    )

    # "Starting" point in each cell
    focal_points = map(Vector, list(focal_points_as_product))

    # Points in first cell
    points_in_first_cell = cell_of_given_size(cell_size)

    # List of list of vectors
    cells_as_vectors = [[focal_point + delta for delta in points_in_first_cell]
                        for focal_point in focal_points]

    # List of list of names (as integers)
    cells = [[vector_to_name(qubit_vector, qubits_in_each_dimension) for qubit_vector in cell]
             for cell in cells_as_vectors]

    return Tessellation(cells)


def vector_to_name(qubit_vector: Vector, qubits_in_each_dimension: List[int]):
    """Find the point in a lexicographic order for a vector.

    This turns a vector in the lattice into an unique "name" (int),
    allowing a linear collection of qubits to represent a lattice.
    """
    def sum_weighted_lengths(index, length, acc):
        """From an initial segment of qubits_in_each_dimension make a weighting."""
        def multiply(acc, entry):
            return entry*acc
        return acc + length * functools.reduce(multiply, qubits_in_each_dimension[index+1:], 1)

    def unpack(acc, index_entry):
        return sum_weighted_lengths(index_entry[0], index_entry[1], acc)

    return functools.reduce(unpack, enumerate(qubit_vector.entries), 0)


__all__ = ["Tessellation", "one_dimensional", "n_dimensional"]
