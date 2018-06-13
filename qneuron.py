# Script for generating quantum neuron circuit (see proposal)

import numpy as np
import json
import time

from pyquil.quil import Program
from pyquil.gates import RY, RZ, Y, NOT, H, CNOT, MEASURE
from pyquil.api import QVMConnection
from pyquil.parameters import Parameter, quil_sin, quil_cos
from pyquil.device import Device
from pyquil.api import CompilerConnection

qvm = QVMConnection()

# define matrix forms of the new gates
theta = Parameter('theta')
cmiy_matrix = np.array([[1, 0, 0, 0], 
                        [0, 1, 0, 0], 
                        [0, 0, 0, -1], 
                        [0, 0, 1, 0]])
ciy_matrix = np.array([[1, 0, 0, 0], 
                       [0, 1, 0, 0], 
                       [0, 0, 0, 1], 
                       [0, 0, -1, 0]])
cry_matrix = np.array([[1, 0, 0, 0], 
                       [0, 1, 0, 0], 
                       [0, 0, quil_cos(theta/2), -quil_sin(theta/2)], 
                       [0, 0, quil_sin(theta/2), quil_cos(theta/2)]])

# define controlled iy gates:
def add_new_gates(pq_prog):
    pq_prog.defgate("CRY", cry_matrix, [theta])
    pq_prog.defgate("C-MINUS-IY", cmiy_matrix)
    pq_prog.defgate("C-IY", ciy_matrix)
    return pq_prog

# Wrapper functions so that these gates act just like the other gates that are imported from pyquil.gates
def CRY(theta, q0, q1):
    return ("CRY({}) {} {}".format(theta, q0, q1))
def CMIY(q0, q1):
    return ("C-MINUS-IY {} {}".format(q0, q1))
def CIY(q0, q1):
    return ("C-IY {} {}".format(q0, q1))
def DOUBLERY(w, beta, q0, q1, q2):
    """
    w is the input vector as a list.
    """
    return Program(CRY(4*w[0], q0, q2), CRY(4*w[1], q1, q2), RY(beta, q2))
def DOUBLERYINV(w, beta, q0, q1, q2):
    """
    w is the input vector as a list.
    """
    return Program(RY(-beta, q2), CRY(-4*w[1], q1, q2), CRY(-4*w[0], q0, q2))

# Function which generates a Program object for the quantum neuron circuit
def make_neuron(w, b, inputs, training, ancilla, output):
    beta = np.pi/4. + b - w[0] - w[1]
    neuron_prog = add_new_gates(Program())
    
    neuron_prog += Program(H(inputs[0]), H(inputs[1]), CNOT(inputs[0], training), CNOT(inputs[1], training))
    
    neuron_prog += DOUBLERY(w, beta, inputs[0], inputs[1], ancilla[0])
    neuron_prog += CMIY(ancilla[0], ancilla[2])
    neuron_prog += DOUBLERYINV(w, beta, inputs[0], inputs[1], ancilla[0])
    neuron_prog += CMIY(ancilla[2], output)
    
    neuron_prog += DOUBLERYINV(w, beta, inputs[0], inputs[1], ancilla[1])
    neuron_prog += CIY(ancilla[1], ancilla[2])
    neuron_prog += DOUBLERY(w, beta, inputs[0], inputs[1], ancilla[1])
    return neuron_prog

# Load device information and generate compiler object
with open('19Q-Acorn.json', 'r') as infile:
    dev_data = json.load(infile)
acorn = Device('19Q-Acorn', dev_data)
compiler = CompilerConnection(acorn)

# Helper function which prints the status of the compilation
def print_job_stats(job):
    print("Gate depth: {}\nGate volume: {}\nTopological Swaps: {}\nMultiq gate depth: {}".format(job.gate_depth(), job.gate_volume(), job.topological_swaps(), job.multiqubit_gate_depth()))

# Helper function for checking the quality of an embedding
def check_compilation(inputs, training, ancilla, output, cmp=compiler):
    qnn_prog = make_neuron([0, 1], np.pi/3., inputs, training, ancilla, output)
    qubits = list(inputs + [training] + ancilla + [output])
    qnn_prog += Program([MEASURE(xx, xx) for xx in qubits])
    compiled_result = compiler.compile_async(Program(qnn_prog))
    job = compiler.get_job(compiled_result)
    job = wait_for_job(compiled_result)
    #print_job_stats(job)
    return job

if __name__ == "__main__":
	check_compilation(inputs=[0,1], training=2, ancilla=[4, 5, 6], output=7)
