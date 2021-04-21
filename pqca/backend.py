import dataclasses
import random

from qiskit import (
    Aer,
    execute,
    QuantumCircuit
)

from .exceptions import BackendError


def AerQasmSimulator(circuit: QuantumCircuit):
    circuit.measure_all()
    results = execute(circuit, Aer.get_backend(
        "qasm_simulator"
    ), shots=1).result()
    if results.success:
        final_state_as_string = list(results.get_counts(circuit).keys())[0]
        return [int(x) for x in final_state_as_string[::-1]]
    else:
        raise BackendError(results.status)