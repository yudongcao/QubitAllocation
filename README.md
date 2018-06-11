# Qubit Allocation
Given a description of the one-qubit and two-qubit fidelities of a given quantum hardware,
as well as the quantum circuit we want to run, 
this algorithm uses simulated annealing to allocate abstract qubits to physical qubits to 
maximize the overall fidelity of the computation. 

As it will be used in conjunction with another path-finding algorithm, we use annealing to
allocate an arbitrary number of qubits, and return a Python dictionary with their respective allocations.

## embedding.py
This is a randomized algorithm that uses a process similar to simulated annealing to return a full
allocation of a given circuit's qubits. However, it relies on the Rigetti Forest QPU to give fidelity
estimates for the allocations, and it always rejects worse allocations. This can be improved by accepting
worse allocations with certain probabilities to ensure we don't get caught at a local max. Usage as well as
graphs can be seen at the bottom of the file which show the progression of overall fidelity as our algorithm proceeds.
