"""Expose ways of evaluating circuits."""

from typing import List, Callable
import qiskit as qskt
from . import exceptions


def qiskit(backend=qskt.Aer.get_backend("qasm_simulator")) -> Callable[[qskt.QuantumCircuit], List[int]]:
    """Transform a qiskit backend into a backend suitable for an Automaton.

    Args:
        backend (qisket backend, optional): A qiskit backend. Defaults to qiskit.Aer.get_backend("qasm_simulator").

    Raises:
        exceptions.BackendError: Any non-successful result will be raised as an exception.

    Returns:
        Callable[[qskt.QuantumCircuit], List[int]]: A function that evaluates a given circuit, returning the list of classical bits.
    """
    def run_circuit_on_backend(circuit: qskt.QuantumCircuit) -> List[int]:
        circuit.measure_all()
        results = qskt.execute(circuit, backend, shots=1).result()
        if results.success:
            final_state_as_string = list(results.get_counts(circuit).keys())[0]
            return [int(x) for x in final_state_as_string[::-1]]
        raise exceptions.BackendError(results.status)
    return run_circuit_on_backend


# Currently Rigetti's python libraries do not support converting from Qasm to Quil
# You can, however, use the website / javascript library found at
# https://quantum-circuit.com/qasm2pyquil
# to create a python snippet that builds the circuit.

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
