"""Create a tessellation from a list of qubits."""

from __future__ import annotations
from typing import List, Callable, Tuple, Iterable
import itertools
import functools
from . import exceptions
from .vector import Vector


class Tessellation:
    """Describes how to partition the lattice into cells.

    This is a list of lists of qubits (expressed as integers) that also performs some validation.
    """

    size: int
    cells: List[List[int]]

    def __init__(self, cells: List[List[int]]):
        """Treat a list of cells as a tessellation.

        Args:
            cells (List[List[int]]): List of cells, each cell being a list of ints

        Raises:
            exceptions.NoCellsException: There should be at least one cell
            exceptions.EmptyCellException: The first cell must be non-empty
            exceptions.PartitionUnevenlyCoversQubits: All qubits must be used at most once
            exceptions.IrregularCellSize: All cells must be the same size
        """
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

    def shifted_by(self, amount=1) -> Tessellation:
        """Shift the tessellation along by the specified amount.

        Equivalent to calling update_names with a function that adds `amount` to every qubit name.

        Args:
            amount (int, optional): The amount, positive or negative, to increase each qubit's name. Defaults to 1.
                Acts modulo the number of qubits in the tessellation.

        Returns:
            Tessellation: A new tessellation with shifted names.
        """
        return self.update_names(lambda x: x+amount)

    def update_names(self,
                     name_update: Callable[[int], int],
                     rename_modulo_size=True) -> Tessellation:
        """Create a new tessellation by renaming every qubit in the old one.

        The function `name_update` is applied to each current qubit name.
        This renaming will happen modulo the number of qubits unless explicitly asked not to.

        Args:
            name_update (Callable[[int], int]): Function to apply to each name.
            rename_modulo_size (bool, optional): After applying the rename enforce names module the number of qubits.
                Defaults to True.

        Returns:
            Tessellation: A new tessellation with the applied renaming.
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
    """Partition a line of length num_qubits into cells of size cell_size.

    Equivalent to a call to `n_dimensional`.

    Args:
        num_qubits (int): Number of qubits to partition.
        cell_size (int): Number of qubits to fit in each cell.

    Returns:
        Tessellation: Partition of the line into equal-sized cells.
    """
    return n_dimensional([num_qubits], [cell_size])


def _cell_of_given_size(cell_dimension: List[int]) -> List[Vector]:
    """Given a length in each dimension create a cell of that size.

    e.g. a `cell_dimension` of [2,3,4] will create a cell of 24 qubits,
    organised as a 3-dimensional vectors that fill out a cuboid of shape 2 by 3 by 4.

    Args:
        cell_dimension (List[int]): List of widths of each dimension.

    Returns:
        List[Vector]: A list of qubits-as-vectors.
    """
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

    Args:
        qubits_in_each_dimension (List[int]): Width in each dimension.
        cell_size (List[int]): Shape of the cells that will cover all the qubits.

    Raises:
        exceptions.IrregularCoordinateDimensions: The cells must evenly cover the whole space.

    Returns:
        Tessellation: A partition of the large space into cells, each cell being a list of qubits.
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
    points_in_first_cell = _cell_of_given_size(cell_size)

    # List of list of vectors
    cells_as_vectors = [[focal_point + delta for delta in points_in_first_cell]
                        for focal_point in focal_points]

    # List of list of names (as integers)
    cells = [[_vector_to_name(qubit_vector, qubits_in_each_dimension) for qubit_vector in cell]
             for cell in cells_as_vectors]

    return Tessellation(cells)


def _vector_to_name(qubit_vector: Vector, qubits_in_each_dimension: List[int]) -> int:
    """Find the equivalent point in a lexicographic order from a vector.

    This turns a vector in the lattice into an unique "name" (int),
    allowing a linear collection of qubits to represent a lattice.

    Args:
        qubit_vector (Vector): A vector representing a single qubit.
        qubits_in_each_dimension (List[int]): The width of each dimension.

    Returns:
        int: qubit name, as an integer
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
