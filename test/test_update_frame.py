"""Test the functionality described in update_frame.py."""

# pylint: disable=import-error
import qiskit
import pqca


def test_wind_circuit_around_loop():
    """One gate on each of five cells should be five gates."""
    tes = pqca.tessellation.one_dimensional(10, 2)
    cx_circuit = qiskit.QuantumCircuit(2)
    cx_circuit.cx(0, 1)
    instructions = pqca.update_frame.wind_circuit_around_loop(cx_circuit, tes)
    assert len(instructions) == 5
