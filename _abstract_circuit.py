""" Abstract class to represent a parameterized Circuit object"""
import copy

from _abstract_gate import AbstractGate


class AbstractCircuitError(Exception):
    pass


class AbstractCircuit(object):
    """ Class for defining the core features of a quantum circuit

    Circuit is an abstract class that captures the basic features of a
    quantum circuit by defining it as a 2D array of abstractGates.

    Attributes:
        basic_block (list):
            An 2D list of AbstractGates, where each row corresponds
            to layer (depth 1 circuit).
        n_qubits (integer):
            Number of qubits in the circuit register
        n_parameters (integer):
            Number of parameters
    """

    def __init__(self, n_qubits, n_blocks=1):
        """
        Inits an AbstractCircuit.

        The init function

        Args:
            n_qubits: number of qubits of the circuit register
            n_parameters (integer, optional): number of parameters involved
            in the circuit
        """
        if not isinstance(n_qubits, int):
            raise AssertionError('number of qubits must be an integer.')
        if not isinstance(n_blocks, int) or n_blocks < 1:
            raise ValueError('number of qubits must be a positive integer.')
        self.n_qubits = n_qubits
        self.n_blocks = n_blocks
        self.basic_block = []
        self.n_variables = 0
        self.n_constants = 0

    def empty(n_qubits):
        """
            Returns:
                multiplative identity circuit
        """
        return AbstractCircuit(n_qubits, b_blocks=1)

    def get_n_parameters(self, is_variational=False):
        """
        Return number of constants or number of n_variables

        Args:
            is_variational (bool)

        """
        if is_variational:
            return self.n_variables
        else:
            return self.n_constants

    def _add_layer(self, layer):
        """
        Add layer of gates to the circuit basic_block

        Args:
            layer (list):
                layer of gates to be added
        """
        if layer == []:
            raise ValueError('Cannot add empty layer')
        for gate in layer:
            if not isinstance(gate, AbstractGate):
                raise AssertionError('Invalid layer: elements of layer' +
                                     'not valid AbstractGates')
            if gate.get_is_variational():
                if any(ind + 1 > self.n_variables for ind in
                       gate.get_indexes()):
                    self.n_variables = max(gate.get_indexes()) + 1
            else:
                if any(ind + 1 > self.n_constants for ind in
                       gate.get_indexes()):
                    self.n_constants = max(gate.get_indexes()) + 1

        self.basic_block.append(layer)

    # def __imul__(self, other):
    #     """
    #     In place multiply (*=) circuits with other circuits

    #     Args:
    #         other (AbstractCircuit)
    #     """
    #     if layer == []:
    #         raise AssertionError('Cannot add empty layer')
    #     # need to check if the layer contain only gates
    #     self.basic_block.append(layer)

    def __str__(self):
        string_rep = ''
        for n, layer in enumerate(self.basic_block):
            string_rep += 'layer {0}\n'.format(n)
            for gate in layer:
                string_rep += str(gate)+'\n'
        return string_rep

    def __repr__(self):
        return str(self)

    def add_adyacent_gates_layer(self, gate, same_angle=False,
                                 skip_first_qubit=False):
        """
        Add a layer of adyacent gates to a circuit

        Args:

            gate (AbstractGate):
                AbstractGate with span m < n_qubits
            same_angle (bool):
                assign same angle to all the single_rotation gates
            skip_first_qubit (boolean):
                start to apply gates in the second qubit
        """
        # Check valid gate
        if not isinstance(gate, AbstractGate):
            raise AssertionError('Gate is not a valid AbstractGate')

        # Check if span is not larger than size of the register
        span = gate.get_span()

        if span > self.n_qubits:
            raise ValueError('The gate span is greater than n_qubits')

        # fix index of first qubit for the gate
        start = int(skip_first_qubit)

        n_parameters = self.get_n_parameters(gate.get_is_variational())
        # build layer
        gate_layer = []

        # compute number of adyacent gates and gate indexes
        n_gates = (self.n_qubits - start) // span
        list_qubits = [start + x * span for x in list(range(0, n_gates))]

        for m, n in enumerate(list_qubits):
            gate = copy.deepcopy(gate)
            gate.assign_qubit_indexes(list(range(n, n + span)))

            if same_angle is True:
                indexes = list(range(n_parameters,
                                     n_parameters +
                                     gate.get_n_parameters()))
            else:
                indexes = list(range(n_parameters +
                                     m*gate.get_n_parameters(),
                                     n_parameters +
                                     (m+1)*gate.get_n_parameters()))
            gate.assign_parameter_indexes(indexes)
            gate_layer.append(gate)

        # add new layer
        self._add_layer(gate_layer)

    def add_gate_as_layer(self, gate, targets):
        """
        Add a gate in a single layer of the circuit

        Args:

            gate (AbstractGate): gate to be added
            targets (list of integers): indexes of the qubits
                upon which the gate acts
        """
        if not isinstance(gate, AbstractGate):
            raise AssertionError('Gate is not a valid AbstractGate')

        if gate.get_span() > self.n_qubits:
            raise ValueError('The gate span is greater than n_qubits')

        if gate.get_span() != len(targets):
            raise ValueError('lens of targets and span must coincide')

        gate.assign_qubit_indexes(targets)

        n_parameters = self.get_n_parameters(gate.get_is_variational())

        indexes = list(range(n_parameters, n_parameters +
                             gate.get_n_parameters()))

        gate.assign_parameter_indexes(indexes)

        self._add_layer([gate])
