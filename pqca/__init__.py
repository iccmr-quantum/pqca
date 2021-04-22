"""Partitioned Quantum Cellular Automata.

A quantum cellular automaton (QCA) iteratively applies some update circuit to some initial state.
The initial state is defined on a lattice, and usually the update step is restricted so that each
qubit can only affect its neighbours during the update step. A partitioned quantum cellular
automaton (PQCA) derives its update circuit by partitioning the lattice into cells, and then
applying the same circuit to each cell. The full update circuit is created by composing several
such partitions.

This module allows for the easy creation of such update circuits, and the PQCA class wraps the
state and update circuits together alongside a link to a TODO
"""

from typing import Callable, List
import random
from dataclasses import dataclass
from qiskit import QuantumCircuit
from .update_frame import UpdateFrame
from .tessellation import *
from .exceptions import *


class PQCA:
    """Partitioned Quantum Cellular Automaton.

    initial_state: a list of 1s and 0s, first bit indicates sate of qubit 0 etc.
    frames: a list of UpdateFrames
    backend: a function that runs a (preparation and update) circuit
    """

    def __init__(self, initial_state: list,
                 frames: List[UpdateFrame], backend: Callable[[QuantumCircuit], List[int]]):
        """PQCA with a given initial state, update frames, and backend.

        The initialisation and update circuit is constructed from the current state
        and the update frames."""
        self.frames = frames
        self.backend = backend
        self.update_instruction = [instruction for
                                   instructions in map(lambda f: f.full_circuit_instructions, self.frames) for
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
        """Combined preparation and update circuit."""
        return self.preparation_circuit + self.update_circuit

    def tick(self):
        """Internal function to update the state without returning anything"""
        assert self.backend, "Backend not yet assigned"
        next_pattern = self.backend(self.combined_circuit)
        self.state = next_pattern

    def iterate(self, number_of_iterations=1):
        """Update the state a certain number of times, returning
        a list of states reached along the way, including the final state"""
        pattern_sequence = []
        for _ in range(0, number_of_iterations):
            self.tick()
            pattern_sequence.append(self.state.copy())
        return pattern_sequence

    def __str__(self):
        frame_string = f"[{','.join([str(frame) for frame in self.frames])}]"
        return f"PQCA(state={self.state}, frames={frame_string})"


def random_bits(how_many: int, seed: int):
    "Return a seeded-random list of 0s and 1s"
    random.seed(seed)
    return [random.choice([True, False]) for q in range(0, how_many)]


def pattern_preparation_circuit(pattern: list):
    """From a list of 0s and 1s create a circuit that encodes this information."""
    circuit = QuantumCircuit(len(pattern))
    for (qubit, boolean_value) in list(enumerate(pattern)):
        if boolean_value:
            circuit.x(qubit)
    return circuit


__all__ = ["random_bits", "PQCA"]
