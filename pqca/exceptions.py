"""Exceptions for the PQCA module."""


class PQCAException(Exception):
    """Base exception class for the pqca module."""


class TooLittleDataForUpdateFrame(PQCAException):
    """Too few arguments given."""

    def __init__(self):
        """Create exception."""
        super().__init__("No circuit, in any format, was provided.")


class TooMuchDataForUpdateFrame(PQCAException):
    """Too many arguments given."""

    def __init__(self):
        """Create exception."""
        super().__init__("Data given in multiple formats; need exactly one.")


class PartitionUnevenlyCoversQubits(PQCAException):
    """The partition must contain each qubit exactly once."""

    def __init__(self, cells):
        """Create exception."""
        super().__init__(
            f"Each qubit must appear exactly once in {cells}.")


class EmptyCellException(PQCAException):
    """Each cell must not be empty."""

    def __init__(self):
        """Create exception."""
        super().__init__("Cells cannot be empty.")


class NoCellsException(PQCAException):
    """There must be at least one cell."""

    def __init__(self):
        """Create exception."""
        super().__init__("There must be at least one cell.")


class IrregularCoordinateDimensions(PQCAException):
    """Two coordinates must be of the same dimension to be compared."""

    def __init__(self, coordinate_1, coordinate_2):
        """Create exception."""
        super().__init__(
            f"{coordinate_1} and {coordinate_2} " +
            "must be of the same length, and divide component-wise.")


class IrregularCellSize(PQCAException):
    """Each cell must be the same size."""

    def __init__(self, cells):
        """Create exception."""
        super().__init__(f"Not all cells in {cells} are of the same size.")


class CircuitWrongShapeForCell(PQCAException):
    """The circuit must be applied to qubits 0...(n-1)."""

    def __init__(self, qubits, size_cell):
        """Create exception."""
        super().__init__(f"Could not apply circuit with qubits {qubits} \
            to cell of size {size_cell}")


class BackendError(PQCAException):
    """Pass backend errors through to user."""
