"""Tests for _qubit_operator.py."""
import copy

import unittest

from _abstract_circuit import AbstractCircuit
from _abstract_gate import AbstractGate


def build_n_qubit_circuit_test(n, option):
    """ Build a circuit test for an n qubit register
    with a block comprising 2 layers of single qubit rotations
    interleaved with odd and even layers of adjayent two qubit gates

    Args:
        n (integer): number of qubits
        option (boolean): choose to have (or not) the same parameters
            per layer
    """
    single_qubit_gate = AbstractGate('X', 1, 10.0, 1, False)
    two_qubit_gate = AbstractGate('ZZ', 2, 40.0, 1, True)
    circuit_example = AbstractCircuit(n)
    # add first layer of single qubit rotations
    circuit_example.add_adyacent_gates_layer(single_qubit_gate, option)
    # add even layer of two qubit gates
    circuit_example.add_adyacent_gates_layer(two_qubit_gate, option, False)
    # add second layer of single qubit rotations
    circuit_example.add_adyacent_gates_layer(single_qubit_gate, option)
    # add odd layer of two qubit gates
    circuit_example.add_adyacent_gates_layer(two_qubit_gate, option, True)

    return circuit_example


class AbstractCircuitTest(unittest.TestCase):

    def test_init_bad_action_n_qubits(self):
        with self.assertRaises(AssertionError):
            _ = AbstractCircuit(10.0, 2)

    def test_init_bad_action_n_blocks(self):
        with self.assertRaises(ValueError):
            _ = AbstractCircuit(10, 2.0)

    def test_bad_action_add_layer_empty(self):
        circuit_example = AbstractCircuit(3)
        with self.assertRaises(ValueError):
            _ = circuit_example._add_layer([])

    def test_bad_action_add_layer_no_gate(self):
        circuit_example = AbstractCircuit(3)
        with self.assertRaises(AssertionError):
            _ = circuit_example._add_layer([1, 2, 3])
        with self.assertRaises(AssertionError):
            _ = circuit_example._add_layer(['1', '2', '3'])

    def test_bad_action_add_adyacent_gates_layer_no_gate(self):
        circuit_example = AbstractCircuit(3)
        with self.assertRaises(AssertionError):
            _ = circuit_example.add_adyacent_gates_layer('string')
        with self.assertRaises(AssertionError):
            _ = circuit_example.add_adyacent_gates_layer(20)
        with self.assertRaises(AssertionError):
            _ = circuit_example.add_adyacent_gates_layer([1, 2, 3])

    def test_bad_action_add_adyacent_gates_layer_nqubits_error(self):
        gate = AbstractGate('ZZZ', 3, 40.0, 1, True)
        circuit_example = AbstractCircuit(2)
        with self.assertRaises(ValueError):
            circuit_example.add_adyacent_gates_layer(gate, True, False)

    def test_bad_action_add_gate_as_layer_no_gate(self):
        circuit_example = AbstractCircuit(3)
        with self.assertRaises(AssertionError):
            _ = circuit_example.add_gate_as_layer('string', [0])
        with self.assertRaises(AssertionError):
            _ = circuit_example.add_gate_as_layer(20, [0])
        with self.assertRaises(AssertionError):
            _ = circuit_example.add_gate_as_layer([1, 2, 3], [0])

    def test_bad_action_add_gate_in_layer_nqubits_error(self):
        gate = AbstractGate('ZZZ', 3, 40.0, 1, True)
        circuit_example = AbstractCircuit(2)
        with self.assertRaises(ValueError):
            circuit_example.add_gate_as_layer(gate, [0, 1, 2])

    def test_bad_action_add_gate_in_layer_wrong_targets_len(self):
        gate = AbstractGate('ZZZ', 3, 40.0, 1, True)
        circuit_example = AbstractCircuit(2)
        with self.assertRaises(ValueError):
            circuit_example.add_gate_as_layer(gate, [0, 1])

    def test_circuit_three_qubits(self):
        single_qubit_gate = AbstractGate('X', 1, 10.0, 1, False)
        two_qubit_gate = AbstractGate('ZZ', 2, 40.0, 1, True)
        circuit = build_n_qubit_circuit_test(3, True)

        self.assertEqual(circuit.get_n_parameters(False), 2)
        self.assertEqual(circuit.get_n_parameters(True), 2)
        for index, gate in enumerate(circuit.basic_block[0]):
            self.assertEqual(gate.__str__(), 'X\t' + str(index) + '\tc0')
        for index, gate in enumerate(circuit.basic_block[2]):
            self.assertEqual(gate.__str__(), 'X\t' + str(index) + '\tc1')
        for index, gate in enumerate(circuit.basic_block[1]):
            self.assertEqual(gate.__str__(), 'ZZ\t0,1\tv0')
        for index, gate in enumerate(circuit.basic_block[3]):
            self.assertEqual(gate.__str__(), 'ZZ\t1,2\tv1')

    def test_circuit_four_qubits(self):
        single_qubit_gate = AbstractGate('X', 1, 10.0, 1, False)
        two_qubit_gate = AbstractGate('ZZ', 2, 40.0, 1, True)
        circuit = build_n_qubit_circuit_test(4, False)

        self.assertEqual(circuit.get_n_parameters(False), 8)
        self.assertEqual(circuit.get_n_parameters(True), 3)
        for index, gate in enumerate(circuit.basic_block[0]):
            self.assertEqual(gate.__str__(), 'X\t' + str(index) + '\tc' +
                             str(index))
        for index, gate in enumerate(circuit.basic_block[2]):
            self.assertEqual(gate.__str__(), 'X\t' + str(index) + '\tc' +
                             str(index+4))
        self.assertEqual(circuit.basic_block[1][0].__str__(), 'ZZ\t0,1\tv0')
        self.assertEqual(circuit.basic_block[1][1].__str__(), 'ZZ\t2,3\tv1')
        self.assertEqual(circuit.basic_block[3][0].__str__(), 'ZZ\t1,2\tv2')

if __name__ == "__main__":
    unittest.main()
