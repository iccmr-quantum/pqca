"""Partitioned Quantum Cellular Automaton."""

from typing import List, Callable
from qiskit import QuantumCircuit
from .update_frame import UpdateFrame


class Automaton:
    """Partitioned Quantum Cellular Automaton.

    initial_state: a list of 1s and 0s, first bit indicates sate of qubit 0 etc.
    frames: a list of UpdateFrames
    backend: a function that runs a (preparation and update) circuit
    """

    def __init__(self, initial_state: list,
                 frames: List[UpdateFrame], backend: Callable[[QuantumCircuit], List[int]]):
        """PQCA with a given initial state, update frames, and backend.

        The initialisation and update circuit is constructed from the current state
        and the update frames.
        """
        self.frames = frames
        self.backend = backend
        frame_instructions = map(
            lambda f: f.full_circuit_instructions, self.frames)
        self.update_instruction = [instruction for
                                   instructions in frame_instructions for
                                   instruction in instructions]

        size = len(initial_state)

        self.state = initial_state

        self.update_circuit = QuantumCircuit(size)
        for instruction, qargs, cargs in self.update_instruction:
            self.update_circuit.append(instruction, qargs, cargs)

    @property
    def preparation_circuit(self):
        """Circuit for preparing a register of qubits into the current state."""
        return pattern_preparation_circuit(self.state)

    @property
    def combined_circuit(self):
        """Combine preparation and update circuit."""
        return self.preparation_circuit + self.update_circuit

    def tick(self):
        """Update the state without returning anything."""
        assert self.backend, "Backend not yet assigned"
        next_pattern = self.backend(self.combined_circuit)
        self.state = next_pattern

    def iterate(self, number_of_iterations=1):
        """Iterate and return new each state reached."""
        pattern_sequence = []
        for _ in range(0, number_of_iterations):
            self.tick()
            pattern_sequence.append(self.state.copy())
        return pattern_sequence

    def __str__(self):
        """Represent as string."""
        frame_string = f"[{','.join([str(frame) for frame in self.frames])}]"
        return f"PQCA(state={self.state}, frames={frame_string})"


def pattern_preparation_circuit(pattern: list):
    """Create a circuit that encoding the starting state."""
    circuit = QuantumCircuit(len(pattern))
    for (qubit, boolean_value) in list(enumerate(pattern)):
        if boolean_value:
            circuit.x(qubit)
    return circuit
