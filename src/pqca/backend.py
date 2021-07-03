"""Expose ways of evaluating circuits."""


import qiskit
from . import exceptions


def Aer(circuit: qiskit.QuantumCircuit, qiskit_backend="qasm_simulator"):
    """Expose the qiskit Aer Simulator."""
    circuit.measure_all()
    results = qiskit.execute(circuit, qiskit.Aer.get_backend(
        qiskit_backend
    ), shots=1).result()
    if results.success:
        final_state_as_string = list(results.get_counts(circuit).keys())[0]
        return [int(x) for x in final_state_as_string[::-1]]
    raise exceptions.BackendError(results.status)


# Currently Rigetti's python libraries do not support converting from Qasm to Quil
# You can, however, use the website / javascript library found at
# https://quantum-circuit.com/qasm2pyquil
# to create a python snippet that builds the circuit.