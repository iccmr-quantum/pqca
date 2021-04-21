"""Exceptions for the PQCA module."""


class PQCAException(Exception):
    """Base exception class for the pqca module."""


class TooLittleDataForUpdateFrame(PQCAException):
    """Too few arguments given."""

    def __init__(self):
        super().__init__("No circuit, in any format, was provided.")


class TooMuchDataForUpdateFrame(PQCAException):
    """Too many arguments given."""

    def __init__(self):
        super().__init__("Data given in multiple formats; need exactly one.")


class PartitionUnevenlyCoversQubits(PQCAException):
    """The partition must contain each qubit exactly once."""

    def __init__(self, qubit, cells, count):
        super().__init__(
            f"Qubit {qubit} appears {count} times in {cells}, must appear exactly once.")

class EmptyCellException(PQCAException):
    """Cells cannot be empty"""
    def __init__(self):
        super().__init__("Cells cannot be empty.")

class IrregularCoordinateDimensions(PQCAException):
    """Two coordinates must be of the same dimension to be compared."""

    def __init__(self, coordinate_1, coordinate_2):
        super().__init__(f"Coordinates {coordinate_1} and {coordinate_2} are of different lengths")

class IrregularCellSize(PQCAException):
    """Each cell must be the same size."""

    def __init__(self, cells):
        super().__init__(f"Not all cells in {cells} are of the same size.")


class CircuitTooBigForCell(PQCAException):
    """The circuit applied to a cell must fit onto that cell."""

    def __init__(self, num_qubits, size_cell):
        super().__init__(f"Could not apply circuit with {num_qubits} qubits \
            to cell of size {size_cell}")

class CircuitWrongShapeForCell(PQCAException):
    """The circuit must be applied to qubits 0...(n-1)"""

    def __init__(self, qubits, size_cell):
        super().__init__(f"Could not apply circuit with qubits {qubits} \
            to cell of size {size_cell}")

class TooManyRegistersInCircuit(PQCAException):
    """Currently only circuits with a single register are supported"""
    def __init__(self, qregs):
        super().__init__(f"Expected only one quantum register, found {qregs}")

class BackendError(PQCAException):
    """Pass backend errors through to user"""