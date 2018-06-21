
"""Functions for gates used in programmable circuits."""
from __future__ import absolute_import

import numpy
import qutip
import scipy


def sq_gate(params):
    """Returns generalized single qubit gate operation

    Args:
        params (numpy.ndarray[float]) : array of rotation angles

    Returns:
        U (Qobj) : unitary for single qubit gate
    """
    U = (qutip.qip.gates.rz(params[0]) *
         qutip.qip.gates.ry(params[1]) *
         qutip.qip.gates.rz(params[2]))
    return U


def sq_gate_2all(params, n_qubits, same_angles=False):
    """Returns generalized single qubit rotations applied to
        all qubits in register

    Args:
        params (numpy.ndarray[float]) : array of rotation angles
        n_qubits (int) : number of qubits
        same_angles (bool) : whether to use same 3 parameters for
                                generalized single qubit rotations
                                on all qubits

    Returns:
        rotations (Qobj) : tensored unitary for applying
                            single qubit rotations for all qubits

    Notes:
        - Single qubit rotations applied to all qubits
            but angles may be different
    """
    all_rotations = [None] * n_qubits
    param_index = 0
    for i in range(n_qubits):
        all_rotations[i] = sq_gate(params[param_index:param_index + 3])

        if same_angles:
            param_index = 0
        else:
            param_index += 3

    rotations = qutip.tensor(all_rotations)
    return rotations


# def single_qubit_yz_rotations(params, n_qubits):
#     """Single qubit rotations (Ry * Rz) applied to all qubits

#     Args:
#         params (numpy.ndarray[float]) : array of rotation angles
#         n_qubits (int) : number of qubits
#         same_angles (bool) : whether to use same parameters for
#                                 all qubits

#     Returns: 
#         rotations (Qobj) : tensored unitary for applying
#                             Ry * Rz rotations for all qubits
#     """
#     all_rotations = [None] * n_qubits
#     param_index = 0
#     for i in range(n_qubits):
#         all_rotations[i] = (qutip.qip.gates.ry(params[param_index]) *
#                             qutip.qip.gates.rz(params[param_index + 1]))

#         if same_angles:
#             param_index = 0
#         else:
#             param_index += 2

#     rotations = qutip.tensor(all_rotations)
#     return rotations


# def single_qubit_xz_rotations(params, n_qubits):
#     """Single qubit rotations (Rx * Rz) applied to all qubits

#     Args:
#         params (numpy.ndarray[float]) : array of rotation angles
#         n_qubits (int) : number of qubits
#         same_angles (bool) : whether to use same parameters for
#                                 all qubits

#     Returns: 
#         rotations (Qobj) : tensored unitary for applying
#                             Rx * Rz rotations for all qubits
#     """
#     all_rotations = [None] * n_qubits
#     param_index = 0
#     for i in range(n_qubits):
#         all_rotations[i] = (qutip.qip.gates.rx(params[param_index]) *
#                             qutip.qip.gates.rz(params[param_index + 1]))

#         if same_angles:
#             param_index = 0
#         else:
#             param_index += 2

#     rotations = qutip.tensor(all_rotations)
#     return rotations


# def single_qubit_z_rotations(params, n_qubits):
#     """Single qubit z rotations applied to all qubits

#     Args:
#         params (numpy.ndarray[float]) : array of rotation angles
#         n_qubits (int) : number of qubits
#         same_angles (bool) : whether to use same parameters for
#                                 all qubits

#     Returns: 
#         rotations (Qobj) : tensored unitary for applying
#                             Rz rotations for all qubits
#     """
#     all_rotations = [None] * n_qubits
#     param_index = 0
#     for i in range(n_qubits):
#         all_rotations[i] = qutip.qip.gates.rz(params[param_index])

#         if same_angles:
#             param_index = 0
#         else:
#             param_index += 1

#     rotations = qutip.tensor(all_rotations)
#     return rotations


def controlled_U(params, n_qubits, control, target):
    """Returns controlled-U operation on n-qubit register
    where U is a generalized single qubit gate

    Args:
        params (numpy.ndarray[float]) : array of arbitrary rotation angles
        n_qubits (int) : number of qubits
        control (int) : index of control qubit
        target (int) : index of target qubit

    Returns:
        U (Qobj) : controlled-U operation
    """
    U = qutip.qip.gates.controlled_gate(sq_gate(params),
                                        n_qubits,
                                        control,
                                        target,
                                        control_value=1)
    return U

def controlled_Rx(params, n_qubits, control, target):
    """Returns controlled-Rx gate operation on n-qubit register

    Args:
        params (numpy.ndarray[float]) : array of Rx angles
        n_qubits (int) : number of qubits
        control (int) : index of control qubit
        target (int) : index of target qubit

    Returns:
        U (Qobj) : controlled-Rx operation
    """
    U = qutip.qip.gates.controlled_gate(qutip.qip.gates.rx(params),
                                        n_qubits,
                                        control,
                                        target,
                                        control_value=1)
    return U

def controlled_Ry(params, n_qubits, control, target):
    """Returns controlled-Ry gate operation on n-qubit register

    Args:
        params (numpy.ndarray[float]) : array of Ry angles
        n_qubits (int) : number of qubits
        control (int) : index of control qubit
        target (int) : index of target qubit

    Returns:
        U (Qobj) : controlled-Ry operation
    """
    U = qutip.qip.gates.controlled_gate(qutip.qip.gates.ry(params),
                                        n_qubits,
                                        control,
                                        target,
                                        control_value=1)
    return U

def controlled_Rz(params, n_qubits, control, target):
    """Returns controlled-Rz gate operation on n-qubit register

    Args:
        params (numpy.ndarray[float]) : array of Rz angles
        n_qubits (int) : number of qubits
        control (int) : index of control qubit
        target (int) : index of target qubit

    Returns:
        U (Qobj) : controlled-Rz operation
    """
    U = qutip.qip.gates.controlled_gate(qutip.qip.gates.rz(params),
                                        n_qubits,
                                        control,
                                        target,
                                        control_value=1)
    return U




# if __name__ == "__main__":

#     p = numpy.array([1., 2., 3.])
#     test = single_qubit_rotations(p, 3, same_angles=True)
#     print(test)
