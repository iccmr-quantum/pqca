"""Partitioned Quantum Cellular Automaton."""

from typing import List, Callable
from qiskit import QuantumCircuit
import qiskit
from .update_frame import UpdateFrame


class Automaton:
    """Partitioned Quantum Cellular Automaton.

    Use `next(automaton)` to advance and return the new state.

    Has an internal state that is updated by applying the update circuit.
    The update circuit is formed by sequentially applying the update frames,
    and then measuring the qubits.

    The evaluation of the circuit is performed by the supplied backend.
    """

    def __init__(self, initial_state: List[int],
                 frames: List[UpdateFrame], backend: Callable[[QuantumCircuit], List[int]]):
        """Automaton with a given initial state, update frames, and backend.

        Use `next(automaton)` to advance and return the new state.

        Args:
            initial_state (List[int]): List of 0s and 1s indicating starting state.
            frames (List[UpdateFrame]): List of update frames to be applied in sequence as the update step.
            backend (Callable[[QuantumCircuit], List[int]]): A function that evaluates a
                quantum circuit once and returns the resulting list of classical bits.
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
    def preparation_circuit(self) -> qiskit.QuantumCircuit:
        """Circuit for preparing a register of qubits into the current state."""
        return _pattern_preparation_circuit(self.state)

    @property
    def combined_circuit(self) -> qiskit.QuantumCircuit:
        """Combine preparation and update circuit."""
        return self.preparation_circuit + self.update_circuit

    def _tick(self) -> None:
        """Update the state without returning anything."""
        assert self.backend, "Backend not yet assigned"
        next_pattern = self.backend(self.combined_circuit)
        self.state = next_pattern

    def __next__(self) -> List[int]:
        """Yield the next state after applying the update circuit.

        Returns:
            List[int]: The new state of the Automaton
        """
        self._tick()
        return self.state

    def __str__(self) -> str:
        """Represent as string."""
        frame_string = f"[{','.join([str(frame) for frame in self.frames])}]"
        return f"PQCA(state={self.state}, frames={frame_string})"


def _pattern_preparation_circuit(pattern: List[int]) -> qiskit.QuantumCircuit:
    """Create a circuit that encodes the given classical state.

    Args:
        pattern (List[int]): A list of 0s and 1s.

    Returns:
        qiskit.QuantumCircuit: A circuit that encodes the given classical bits as
            the tensor product of 0 and 1 states.
    """
    circuit = QuantumCircuit(len(pattern))
    for (qubit, boolean_value) in list(enumerate(pattern)):
        if boolean_value:
            circuit.x(qubit)
    return circuit


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
