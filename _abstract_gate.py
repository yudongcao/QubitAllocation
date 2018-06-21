""" Abstract class to represent a parameterized Gate object"""


class AbstractGateError(Exception):
    pass


class AbstractGate(object):
    """ Class for defining the core features of a parameterized Gate

    Gate is an abstract class that capture the basic features of
    a gate.

    Attributes:
        name (string):
            A name uniquely identifying the name of the gate. Gates
            describing product of Pauli matrices are uniquely reserved
            for exponential of Pauli operators e.g. 'XX' corresponds
            to exp(-i parameters XX/2).
        span (integer):
            An integer describing the number of qubits the gate acts
            upon. In the previous example that corresponds to 2
        n_parameters (integer):
            Number of parameters involved in the gate
        variational (boolean):
            Boolean indicating whether the gate acts as a variational
            gate or not. e.g. True

    """

    def __init__(self, name, span, time=0.0, n_parameters=0,
                 is_variational=False, gate_type='default'):
        """
        Inits a parameterized Gate.

        The init function

        Args:
        name (string): a string uniquely identifying the name of the gate.
            Gates describing product of Pauli matrices are uniquely
            reserved for exponential of Pauli operators e.g. 'XX'
            corresponds to exp(-i parameters XX/2).
        span (integer): an integer describing the number of qubits
            the gate acts upon.
        time (float): a float corresponding to the time required to execute
            the gate, according to some parameterized scale.
        n_parameters (integer, optional): number of parameters involved
            in the gate
        is_variational (boolean): boolean indicating whether the gate acts
            as a variational gate or not. e.g. True
        """
        if not isinstance(name, str):
            raise ValueError('Name must be a string.')
        if not isinstance(span, int):
            raise ValueError('span must be an integer.')
        if not isinstance(time, float) or time < 0.0:
            raise ValueError('time must be real and non-negative')
        if not isinstance(n_parameters, int):
            raise ValueError('n_parameters must be an integer.')
        if not isinstance(is_variational, bool):
            raise ValueError('variational must be a boolean.')
        if not isinstance(gate_type, str):
            raise ValueError('Gate type must be a string.')
        self.name = name
        self.span = span
        self.time = time
        self.n_parameters = n_parameters
        self.is_variational = is_variational
        self.targets = []
        self.indexes = []
        self.gate_type = gate_type

    def get_name(self):
        return self.name

    def get_span(self):
        return self.span

    def get_n_parameters(self):
        return self.n_parameters

    def get_time(self):
        return self.time

    def get_is_variational(self):
        return self.is_variational

    def get_targets(self):
        return self.targets

    def get_indexes(self):
        return self.indexes

    def get_type(self):
        return self.gate_type

    def assign_parameter_indexes(self, indexes):
        """
        Assign the indexes of the parameters associated to a gate

        Args:
        indexes (list): list of integers associated to indexes
        in some parameter array
        """
        if not isinstance(indexes, list):
            raise ValueError('indexes must be a list of integers')
        if len(indexes) != self.n_parameters:
            raise AbstractGateError("Number of parameters is incorrect")
        self.indexes = indexes

    def assign_qubit_indexes(self, indexes):
        """
        Assign the indexes of the qubits targeted by the gate

        Args:
        targets (list): list of integers associated to indexes
        in some parameter array
        """
        if not isinstance(indexes, list):
            raise ValueError('indexes must be a list of integers')
        if len(indexes) != self.span:
            raise AbstractGateError("Number of qubits for gate is incorrect")
        self.targets = indexes

    def __str__(self):
        targets_str = ''
        indexes_str = ''
        if self.get_is_variational() is True:
            var_type = 'v'
        else:
            var_type = 'c'
        for t in self.targets:
            targets_str += str(t)+','
        for i in self.indexes:
            indexes_str += var_type+str(i)+','
        return ("{0}\t{1}\t{2}".format(self.name, targets_str[:-1],
                                       indexes_str[:-1]))

    def __repr__(self):
        return str(self)
