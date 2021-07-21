"""Exceptions for the PQCA module."""


class PQCAException(Exception):
    """Base exception class for the pqca module."""


class PartitionUnevenlyCoversQubits(PQCAException):
    """The partition must contain each qubit exactly once."""

    def __init__(self, cells):
        """Create PartitionUnevenlyCoversQubits exception."""
        super().__init__(
            f"Each qubit must appear exactly once in {cells}.")


class EmptyCellException(PQCAException):
    """Each cell must not be empty."""

    def __init__(self):
        """Create EmptyCellException exception."""
        super().__init__("Cells cannot be empty.")


class NoCellsException(PQCAException):
    """There must be at least one cell."""

    def __init__(self):
        """Create NoCellsException exception."""
        super().__init__("There must be at least one cell.")


class IrregularCoordinateDimensions(PQCAException):
    """Two coordinates must be of the same dimension to be compared."""

    def __init__(self, coordinate_1, coordinate_2):
        """Create IrregularCoordinateDimensions exception."""
        super().__init__(
            f"{coordinate_1} and {coordinate_2} " +
            "must be of the same length, and divide component-wise.")


class IrregularCellSize(PQCAException):
    """Each cell must be the same size."""

    def __init__(self, cells):
        """Create IrregularCellSize exception."""
        super().__init__(f"Not all cells in {cells} are of the same size.")


class CircuitWrongShapeForCell(PQCAException):
    """The circuit must be applied to qubits 0...(n-1)."""

    def __init__(self, qubits, size_cell):
        """Create CircuitWrongShapeForCell exception."""
        super().__init__(f"Could not apply circuit with qubits {qubits} \
            to cell of size {size_cell}")


class BackendError(PQCAException):
    """Pass backend errors through to user."""

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