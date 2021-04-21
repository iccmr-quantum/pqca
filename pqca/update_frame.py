"""An UpdateFrame holds cell-circuit and tessellation data.

"""

from qiskit import QuantumCircuit
import re
from .tessellation import Tessellation
from .exceptions import (TooLittleDataForUpdateFrame,
                         TooMuchDataForUpdateFrame,
                         CircuitWrongShapeForCell,
                         TooManyRegistersInCircuit)


class UpdateFrame:
    """Create a large circuit from a tessellated small circuit."""
    cell_circuit: QuantumCircuit
    tessellation: Tessellation
    tessellated_circuit: Tessellation

    def __init__(self,
                 tessellation: Tessellation,
                 qasm_circuit_file: str = None,
                 qasm_data_as_string: str = None,
                 qiskit_circuit: QuantumCircuit = None):
        """Holds the circuit to be applied to each cell in the tessellation.

        """
        # actually want to check if has to_qasm
        count_arguments_not_none: int = len([arg for arg in (
            qasm_circuit_file, qasm_data_as_string, qiskit_circuit) if arg is not None])
        if count_arguments_not_none == 0:
            raise TooLittleDataForUpdateFrame
        elif count_arguments_not_none > 1:
            raise TooMuchDataForUpdateFrame
        if qasm_data_as_string:
            self.cell_circuit = QuantumCircuit.from_qasm_str(
                qasm_data_as_string)
        if qasm_circuit_file:
            self.cell_circuit = QuantumCircuit.from_qasm_file(
                qasm_circuit_file)
        if qiskit_circuit:
            self.cell_circuit = qiskit_circuit

        self.tessellation = tessellation
        self.tessellated_gates = wind_circuit_around_loop(
            self.cell_circuit, self.tessellation)

    def __repr__(self):
        return f"""UpdateFrame(circuit: {self.cell_circuit}
        on each cell of {str(self.tessellation)},
        resulting in circuit {self.tessellated_gates})"""

    def __str__(self):
        return f"UpdateFrame(circuit: {self.cell_circuit} on each cell of {str(self.tessellation)})"


def wind_circuit_around_loop(circuit: QuantumCircuit, tessellation: Tessellation):
    "Returns the tessellated circuit as a sequence of qasm instructions"
    # Need to interpret OpenQasm strings
    # Going to assume that all qubits are referred to as q[\d+]00

    from qiskit.circuit.quantumregister import Qubit, QuantumRegister

    if len(circuit.qubits) > len(tessellation.cells[0]):
        raise CircuitWrongShapeForCell(
            circuit.qubits, len(tessellation.cells[0]))
    next_column = []

    if len(circuit.qregs) > 1:
        raise TooManyRegistersInCircuit(circuit.qregs)

    qreg = QuantumRegister(tessellation.size, circuit.qregs[0].name)

    for cell in tessellation.cells:
        for instruction, qargs, cargs in circuit.data:
            # Create a new instruction pointing at the correct qubits
            instruction_context = instruction, [
                Qubit(qreg, cell[q.index]) for q in qargs], cargs
            next_column.append(instruction_context)
    return next_column


__all__ = ["UpdateFrame"]
