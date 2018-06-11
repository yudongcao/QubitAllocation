from pyquil.api import QVMConnection, CompilerConnection, get_devices
from pyquil.quil import Pragma, Program, shift_quantum_gates
from pyquil.gates import CNOT, H, RZ, RX
import random
import matplotlib.pyplot as plt
import numpy as np


# create a random embedding of 19 qubits
# built specifically for Rigetti 19 qubit machine
def create(n):
    # currently, qubits 2,3,15, and 18 are out of service 
    qubits = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19]
    random.shuffle(qubits)
    return qubits[:n]

# takes a desired embedding and returns a new program with that embedding
def change(program, embedding):
    p_str = program.out()
    qubits = list(program.get_qubits())
    for i in range(len(qubits) -1, -1, -1):
        p_str = p_str.replace(" " + str(qubits[i]) + '\n', " *" + str(embedding[i]) + '\n')
        p_str = p_str.replace(" " + str(qubits[i]) + ' ', " *" + str(embedding[i]) + ' ')
    for i in range(20 - 1, -1, -1):
        p_str = p_str.replace('*' + str(i), str(i))
    return Program(p_str)

# given an embedding randomly change each qubit w/ probablity (sens)
def mix(embedding, sens):
    if sens <= 0:
        return embedding
    mix_list = []
    mix_ind = []
    for i in range(len(embedding)):
        if random.random() > sens:
            mix_ind.append(i)
            mix_list.append(embedding[i])
    random.shuffle(mix_list)
    for i in range(len(mix_ind)):
        embedding[mix_ind[i]] = mix_list[i]
    return embedding

# check 10 random embeddings, run sens/0.05 additional tests, output hightest fidelity
def max_fid(program, embedding, sens):
    global global_mx
    devices = get_devices(as_dict=True)
    acorn = devices['19Q-Acorn']
    compiler = CompilerConnection(acorn)
    
    while True:
        p = change(program, embedding)
        job_id = compiler.compile_async(p)
        job = compiler.wait_for_job(job_id)
        if sens <= 0:
            return global_mx
        else:
            try:
                fid = job.program_fidelity()
                print("fid:", fid)
                break
            except:
                sens -= .05
                continue
        mx = max(fid, max_fid(program, mix(embedding, sens), sens - .05))
        global_mx = max(global_mx, mx)
        max_list.append(global_mx)
        return mx
    
# uses Rigetti QPU to estimate fidelity, and returns the best allocation found
def allocator(program):
    devices = get_devices(as_dict=True)
    acorn = devices['19Q-Acorn']
    compiler = CompilerConnection(acorn)
    res = []
    res_embed = []
    i = 0
    while i <= 10:
        embedding = create(19)
        
        p = change(program, embedding)
        job_id = compiler.compile_async(p)
        job = compiler.wait_for_job(job_id)
        print(embedding)
        try:
            fid = job.program_fidelity()
        
            print('fid:', fid)
            global global_mx
            global_mx = max(global_mx, fid)
            max_list.append(global_mx)

            res.append(fid)
            res_embed.append(embedding)
            i += 1
        except:
            fid = 0
            continue
    mx = max(res)
    mx_embed = res_embed[res.index(mx)]    
    return max_fid(program, mx_embed, 1), mx_embed

# Test on a randomly generated circuit 5 times to show average trend
program = Program(CNOT (9, 14),RZ (-0.743043, 14),CNOT (9, 14),CNOT (12, 16),RZ (-0.743043, 16),CNOT (12, 16),CNOT (16, 2))

max_lists = []
for i in range(5):
    global global_mx
    global_mx = 0.
    global max_lst 
    max_list = []

    allocator(program)
    max_lists.append(max_list)

# change in fidelity over time
plt.figure(figsize=(9, 6))  
plt.xlabel('# calls to compiler', fontsize=16)  
plt.ylabel('maximum fidelity', fontsize=16)  
plt.title('Change in fidelity over time', fontsize=22)  

for lst in max_lists:
    plt.plot(lst)

plt.show()

# average change in fidelity over time
plt.figure(figsize=(9, 6))  

plt.plot(np.mean(np.array(max_lists), axis=0), 'b')

plt.xlabel('# calls to compiler', fontsize=16)  
plt.ylabel('maximum fidelity', fontsize=16)  
plt.title('Change in fidelity over time (Average of 10 trials)', fontsize=22)  

plt.show()
