"""Tests for _qubit_operator.py."""
import copy

import unittest

from _abstract_gate import (AbstractGate,
                            AbstractGateError)

class AbstractGateTest(unittest.TestCase):

    def test_single_qubit_gate_init(self):
        single_qubit_gate = AbstractGate('X', 1, 10.0, 1, False)
        self.assertEqual('X', single_qubit_gate.get_name())
        self.assertEqual(1, single_qubit_gate.get_span())
        self.assertEqual(10.0, single_qubit_gate.get_time())
        self.assertEqual(1, single_qubit_gate.get_n_parameters())
        self.assertEqual(False, single_qubit_gate.get_is_variational())
        self.assertEqual('default', single_qubit_gate.get_type())
        self.assertEqual([], single_qubit_gate.get_indexes())
        self.assertEqual([], single_qubit_gate.get_targets())

    def test_two_qubit_gate_init(self):
        two_qubit_gate = AbstractGate('XX', 2, 10.0, 1, True)
        self.assertEqual('XX', two_qubit_gate.get_name())
        self.assertEqual(2, two_qubit_gate.get_span())
        self.assertEqual(10.0, two_qubit_gate.get_time())
        self.assertEqual(1, two_qubit_gate.get_n_parameters())
        self.assertEqual(True, two_qubit_gate.get_is_variational())
        self.assertEqual('default', two_qubit_gate.get_type())
        self.assertEqual([], two_qubit_gate.get_indexes())
        self.assertEqual([], two_qubit_gate.get_targets())

    def test_assign_parameter_indexes(self):
        gate = AbstractGate('XXY', 3, 10.0, 1, True)
        gate.assign_parameter_indexes([0])
        self.assertEqual([0], gate.get_indexes())

    def test_assign_qubit_indexes(self):
        gate = AbstractGate('XXY', 3, 10.0, 1, True)
        gate.assign_qubit_indexes([0,1,2])
        self.assertEqual([0,1,2], gate.get_targets())

    def test_init_bad_action_name(self):
        with self.assertRaises(ValueError):
            _ = AbstractGate(1, 2, 10.0, 1, True)

    def test_init_bad_action_span(self):
        with self.assertRaises(ValueError):
            _ = AbstractGate('XX', 'J', 10.0, 1, True)

    def test_init_bad_action_time(self):
        with self.assertRaises(ValueError):
            _ = AbstractGate('XX', 1, 'J', 1, True)

    def test_init_bad_action_time_negative(self):
        with self.assertRaises(ValueError):
            _ = AbstractGate('XX', 1, -10.0, 1, True)

    def test_init_bad_action_n_parameters(self):
        with self.assertRaises(ValueError):
            _ = AbstractGate('XX', 1, 10.0, 'J', True)

    def test_init_bad_action_is_variational(self):
        with self.assertRaises(ValueError):
            _ = AbstractGate('XX', 1, -10.0, 1, 2)

    def test_init_bad_action_gate_type(self):
        with self.assertRaises(ValueError):
            _ = AbstractGate('XX', 1, -10.0, 1, False, 4)

    def test_bad_action_assign_parameter_indexes(self):
        gate = AbstractGate('XXY', 3, 10.0, 1, True)
        with self.assertRaises(AbstractGateError):
            _ = gate.assign_parameter_indexes([0, 1, 2])

    def test_bad_action_assign_qubit_indexes(self):
        gate = AbstractGate('XXY', 3, 10.0, 1, True)
        with self.assertRaises(AbstractGateError):
            _ = gate.assign_qubit_indexes([0])

    def test_print_method_one_qubit_variational(self):
        gate = AbstractGate('X', 1, 10.0, 1, True)
        gate.assign_qubit_indexes([0])
        gate.assign_parameter_indexes([1])
        self.assertEqual(gate.__str__(),'X\t0\tv1')

    def test_print_method_one_qubit_constant(self):
        gate = AbstractGate('X', 1, 10.0, 1, False)
        gate.assign_qubit_indexes([0])
        gate.assign_parameter_indexes([1])
        self.assertEqual(gate.__str__(),'X\t0\tc1')

    def test_print_method_three_qubits_variational(self):
        gate = AbstractGate('XXY', 3, 10.0, 1, True)
        gate.assign_qubit_indexes([0,1,2])
        gate.assign_parameter_indexes([1])
        self.assertEqual(gate.__str__(),'XXY\t0,1,2\tv1')

    def test_print_method_three_qubits_constant(self):
        gate = AbstractGate('XXY', 3, 10.0, 1, False)
        gate.assign_qubit_indexes([0,1,2])
        gate.assign_parameter_indexes([1])
        self.assertEqual(gate.__str__(),'XXY\t0,1,2\tc1')

    def test_print_method_three_qubits_variational_two_parameters(self):
        gate = AbstractGate('XXY', 3, 10.0, 2, True)
        gate.assign_qubit_indexes([0,1,2])
        gate.assign_parameter_indexes([1,2])
        self.assertEqual(gate.__str__(),'XXY\t0,1,2\tv1,v2')

    def test_print_method_three_qubits_constant_two_parameters(self):
        gate = AbstractGate('XXY', 3, 10.0, 2, False)
        gate.assign_qubit_indexes([0,1,2])
        gate.assign_parameter_indexes([1,2])
        self.assertEqual(gate.__str__(),'XXY\t0,1,2\tc1,c2')

if __name__ == '__main__':
    unittest.main()