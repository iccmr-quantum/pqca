"""Test the functionality described in update_frame.py."""

# pylint: disable=import-error
import qiskit
import pytest
import pqca


def test_wind_circuit_around_loop():
    """One gate on each of five cells should be five gates."""
    tes = pqca.tessellation.one_dimensional(10, 2)
    cx_circuit = qiskit.QuantumCircuit(2)
    cx_circuit.cx(0, 1)
    instructions = pqca.update_frame._wind_circuit_around_loop(cx_circuit, tes)
    assert len(instructions) == 5


def test_wind_circuit_around_loop_exceptions():
    """Bad arguments fail informatively."""
    tes = pqca.tessellation.one_dimensional(10, 2)
    cx_circuit = qiskit.QuantumCircuit(3)
    with pytest.raises(pqca.exceptions.CircuitWrongShapeForCell):
        pqca.update_frame._wind_circuit_around_loop(cx_circuit, tes)

def test_update_frame_repr():
    """Test the string representation."""
    tes = pqca.tessellation.one_dimensional(10, 2)
    cx_circuit = qiskit.QuantumCircuit(2)
    cx_circuit.cx(0, 1)
    frame = pqca.UpdateFrame(tes, qiskit_circuit=cx_circuit)
    assert len(str(frame)) > 0
