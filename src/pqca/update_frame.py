"""An UpdateFrame holds cell-circuit and tessellation data."""

from typing import List
from qiskit import QuantumCircuit
from qiskit.circuit.quantumregister import Qubit, QuantumRegister
from .tessellation import Tessellation
from .exceptions import (CircuitWrongShapeForCell)


class UpdateFrame:
    """Create a large circuit from a tessellated small circuit."""

    cell_circuit: QuantumCircuit
    tessellation: Tessellation
    full_circuit_instructions: List

    def __init__(self,
                 tessellation: Tessellation,
                 qiskit_circuit: QuantumCircuit):
        """Hold the circuit to be applied to each cell in the tessellation.
        
        Note that you can construct a qiskit circuit via
        * qiskit.QuantumCircuit.from_qasm_str
        * qiskit.QuantumCircuit.from_qasm_file
        """        
        self.cell_circuit = qiskit_circuit

        self.tessellation = tessellation
        self.full_circuit_instructions = _wind_circuit_around_loop(
            self.cell_circuit, self.tessellation)

    def __str__(self):
        """Human-readable string representation."""
        return f"UpdateFrame(circuit: {self.cell_circuit} on each cell of {str(self.tessellation)})"


def _wind_circuit_around_loop(circuit: QuantumCircuit, tessellation: Tessellation):
    """Return the tessellated circuit as a list of instructions.

    Args:
        circuit (QuantumCircuit): Circuit defined on qubits in the first cell, to be tessellated to all cells.
        tessellation (Tessellation): Tessellation of the qubits into cells.

    Raises:
        CircuitWrongShapeForCell: The circuit cannot use more qubits than there are qubits in the first cell.

    Returns:
        List[circuit instructions]: List of instructions that will later be combined into a circuit.
    """
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