"""Test the PQCA class."""

# pylint: disable=import-error
import qiskit
import pqca
import pqca.backend


def test_create_automaton():
    """1-D automaton, no simulation."""
    cx_circuit = qiskit.QuantumCircuit(2)
    cx_circuit.cx(0, 1)
    tes = pqca.tessellation.one_dimensional(10, 2)
    automaton = pqca.Automaton(
        [0]*10, [pqca.UpdateFrame(tes, qiskit_circuit=cx_circuit)], lambda x: [1]*10)
    assert next(automaton) == [1]*10
    assert len(str(automaton)) > 0


def test_aer_backend():
    """Simulate 1-D automaton."""
    cx_circuit = qiskit.QuantumCircuit(2)
    cx_circuit.cx(0, 1)
    tes = pqca.tessellation.one_dimensional(4, 2)
    automaton = pqca.Automaton(
        [1]*4, [pqca.UpdateFrame(tes, qiskit_circuit=cx_circuit)], pqca.backend.qiskit())
    assert next(automaton) == [1, 0]*2
