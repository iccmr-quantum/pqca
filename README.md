# PQCA (Partitioned Quantum Cellular Automata)

A quantum cellular automaton iteratively applies some update circuit to some initial state.
A partitioned quantum cellular automaton (PQCA) derives its update circuit by partitioning
the lattice into cells, and then applying the same circuit to each cell.
The full update circuit is created by composing several such partitions.

This module allows for the easy creation and execution of such automata.
To create an automaton you will need:
 - A starting state (list of 0s and 1s)
 - Update Frames (see pqca.update_frame.py)
 - A simulator / quantum computer (see pqca.backend.py)

An Update Frame is a tessellation and a circuit to be applied
to each cell in that tessellation.
A tessellation just partitions qubits into cells. For example
`pqca.tessellation.one_dimensional(10,2)`
partitions 10 qubits into 5 cells, each of size 2.
The Update Frame would then need to be a circuit on 2 qubits.

The Automaton is called with `automaton.iterate(n)` which will apply the update frames `n` times,
recording the internal state after each application.
Qiskit's Aer simulator backend is provided out-of-the-box.

Here is an example that creates two update frames,
both applying a simple CX gate, but with offset tessellations.
```python
# Create circuit
cx_circuit = qiskit.QuantumCircuit(2)
cx_circuit.cx(0, 1)

# Create tessellation
tes = pqca.tessellation.one_dimensional(10, 2)

# Create update frame
update_1 = pqca.UpdateFrame(tes, qiskit_circuit=cx_circuit)
update_2 = pqca.UpdateFrame(tes.shifted_by(1), qiskit_circuit=cx_circuit)

# Create initial state
initial_state = [1]*10

# Specify a backend
def backend(circuit):
    return pqca.backend.Aer(circuit, "qasm_simulator")

# Create the automaton
automaton = pqca.Automaton(initial_state, [update_1, update_2], backend)

# Iterate the automaton 5 times
automaton.iterate(5)
```