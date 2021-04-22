"""An UpdateFrame holds cell-circuit and tessellation data."""

import re
from typing import List
from qiskit import QuantumCircuit
from qiskit.circuit.quantumregister import Qubit, QuantumRegister
from .tessellation import Tessellation
from .exceptions import (TooLittleDataForUpdateFrame,
                         TooMuchDataForUpdateFrame,
                         CircuitWrongShapeForCell)


class UpdateFrame:
    """Create a large circuit from a tessellated small circuit."""

    cell_circuit: QuantumCircuit
    tessellation: Tessellation
    full_circuit_instructions: List

    def __init__(self,
                 tessellation: Tessellation,
                 qasm_circuit_file: str = None,
                 qasm_data_as_string: str = None,
                 qiskit_circuit: QuantumCircuit = None):
        """Hold the circuit to be applied to each cell in the tessellation."""
        count_arguments_not_none: int = len([arg for arg in (
            qasm_circuit_file, qasm_data_as_string, qiskit_circuit) if arg is not None])
        if count_arguments_not_none == 0:
            raise TooLittleDataForUpdateFrame
        elif count_arguments_not_none > 1:
            raise TooMuchDataForUpdateFrame

        if qasm_data_as_string is not None:
            self.cell_circuit = QuantumCircuit.from_qasm_str(
                qasm_data_as_string)
        if qasm_circuit_file is not None:
            self.cell_circuit = QuantumCircuit.from_qasm_file(
                qasm_circuit_file)
        if qiskit_circuit is not None:
            self.cell_circuit = qiskit_circuit

        self.tessellation = tessellation
        self.full_circuit_instructions = wind_circuit_around_loop(
            self.cell_circuit, self.tessellation)

    def __str__(self):
        """Human-readable string representation."""
        return f"UpdateFrame(circuit: {self.cell_circuit} on each cell of {str(self.tessellation)})"


def wind_circuit_around_loop(circuit: QuantumCircuit, tessellation: Tessellation):
    """Return the tessellated circuit as a list of instructions."""
    if len(circuit.qubits) > len(tessellation.cells[0]):
        raise CircuitWrongShapeForCell(
            circuit.qubits, len(tessellation.cells[0]))
    next_column = []

    qreg = QuantumRegister(tessellation.size, circuit.qregs[0].name)

    for cell in tessellation.cells:
        for instruction, qargs, cargs in circuit.data:
            # Create a new instruction pointing at the correct qubits
            instruction_context = instruction, [
                Qubit(qreg, cell[q.index]) for q in qargs], cargs
            next_column.append(instruction_context)
    return next_column
