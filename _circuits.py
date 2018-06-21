
import numpy
from qutip import *


class ParametrizedCircuit:
    """
    A parametrized (programmable) quantum circuit.
    """
    def __init__(self, parameters, n_repetitions):
        """
        Args:
            parameters (numpy.ndarray) : array of circuit parameters
            n_repetitions (int) : number of circuit block repetitions

        Attributes:
            n_parameters (int) : number of unique circuit parameters
            unitary (numpy.ndarray) : unitary corresponding to circuit
            cost_function (callable) : cost function depending on
                                        parametrized unitaries
        """
        self.parameters = parameters
        self.n_parameters = len(parameters)
        self.n_repetitions
        self.unitary = None
        self.cost_function = None

    # Instance-dependent
    def set_unitary(self, unitary):
        """Sets unitary matrix representation of circuit

        Args:
            unitary (Qobj) : unitary representation of circuit
        """
        self.unitary = unitary

    # TODO! (average fidelity as default?)
    def set_cost_function(self):
        raise NotImplementedError

    # TODO!
    def compute_gradient(self):
        raise NotImplementedError
