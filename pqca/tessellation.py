"""Partition a list of qubits into a tessellation of cells."""
from __future__ import annotations
from typing import List, Callable, Tuple, Iterable
import itertools
from .exceptions import IrregularCellSize, EmptyCellException
from .vector import Vector


class Tessellation:
    """Describes how to partition the lattice into cells
    This is a list of lists of qubits that also performs some data validation"""

    size: int

    def __init__(self, cells: List[int]):
        assert len(cells) > 0, "There must be at least one cell"
        assert len(
            cells[0]) > 0, "There must be at least one qubit in the first cell"
        self.cells = cells
        self.size = sum([len(c) for c in cells])
        # check no qubit appears twice
        set_of_cells = set([c for cell in self.cells for c in cell])
        assert len(
            set_of_cells) == self.size, "At least one qubit appears in more than one cell"
        # check all cells the same size
        assert len(set([len(cell) for cell in cells])
                   ) == 1, "Not all cells are the same size"

    def shifted_by(self, amount=1):
        """Shift the tessellation along by the specified amount."""
        return self.update_names(lambda x: x+amount)

    def update_names(self,
                     name_update: Callable[[int], int],
                     rename_modulo_size=True) -> Tessellation:
        """create a new tessellation by renaming every qubit in the old one.

        This renaming will happen modulo the number of qubits."""
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
        return f"""Tessellation({self.size} qubits as {len(self.cells)} cells, first cell: {self.cells[0]})"""


def line_with_cells(cell_size: int, cell_count: int):
    """Partition a line into a given number of cells of given size."""
    return Tessellation([list(range(i*cell_size, (i+1)*cell_size)) for i in range(0, cell_count)])


def one_dimensional(num_qubits: int, cell_size: int) -> Tessellation:
    """Partition a line of length num_qubits into cells of size cell_size"""
    assert num_qubits % cell_size == 0, "The cell size must divide the number of qubits"
    return line_with_cells(cell_size, int(num_qubits / cell_size))


def cell_of_given_size(cell_dimension: List[int]) -> List[Vector]:
    """Given a length in each dimension create a cell."""
    points_in_first_cell = itertools.product(
        *list(map(lambda d: list(range(0, d)), cell_dimension))
    )

    first_cell_as_vectors = map(lambda t: Vector(
        list(t)), list(points_in_first_cell))
    return list(first_cell_as_vectors)


def n_dimensional(qubits_in_each_dimension: List[int],
                  cell_dimension: List[int]) -> Tessellation:
    """Partition an n-dimensional lattice into n-dimensional cuboids.

    example qubits_in_each_dimension: [5,5,10] for a cuboid of size 5 by 5 by 10
    example cell_dimension: [5,5,2]

    Note that the size of the cell must divide (for each dimension) the number
    of qubits in the lattice.
    """
    for index, length in enumerate(qubits_in_each_dimension):
        assert length % cell_dimension[index] == 0

    number_steps_in_any_dimension = [
        int(a/b) for (a, b) in zip(qubits_in_each_dimension, cell_dimension)]

    # Find the focal (first) point in each cell
    step_data: List[Tuple[int, int]] = zip(
        qubits_in_each_dimension, number_steps_in_any_dimension)

    focal_points_as_product = itertools.product(
        *list(map(lambda step_dim: list(range(0, step_dim[0], step_dim[1])), step_data))
    )

    focal_points = map(Vector, list(focal_points_as_product))

    # Find all the other points from a focal point

    points_in_first_cell = cell_of_given_size(cell_dimension)

    cells_as_vectors = [[focal_point + delta for delta in points_in_first_cell]
                        for focal_point in focal_points]

    print(cells_as_vectors)

    # Need to turn n-dimensional data into a single number
    # This is because our qubits are numbered 0...n
    def multiplicative_rename_scale(dimension: int):
        acc = 1
        for dim in range(0, dimension):
            acc *= qubits_in_each_dimension[dim]
        return acc

    def vector_to_name(qubit_vector: Vector):
        acc = 0
        for index, entry in enumerate(qubit_vector):
            acc += entry*multiplicative_rename_scale(index)
        return acc

    # From a cell described as vectors give a cell as qubit names
    cells = [[vector_to_name(qubit_vector) for qubit_vector in cell]
             for cell in cells_as_vectors]

    return Tessellation(cells)


def blank_lattice(qubits_in_each_dimension: List[int]):
    """Create a lattice of points of the given size."""
    iterators = [range(0, number_in_this_dimension)
                 for number_in_this_dimension in qubits_in_each_dimension]

    def expand_points(list_of_points: List[Vector], iterator: Iterable):
        return [point.extend(next_entry) for point in list_of_points for next_entry in iterator]

    all_points = [Vector(())]
    for iterator in iterators:
        all_points = expand_points(all_points, iterator)

    return all_points
