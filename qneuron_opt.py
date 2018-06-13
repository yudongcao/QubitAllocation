# Optimize the circuit embedding by simulated annealing
#

__author__ = 'Yudong Cao'

from qneuron import *
from hardwaregraph import *

from random import randint, uniform, shuffle
from copy import deepcopy
from math import exp

# Hardware graph of Rigetti
# See Figure 1a at http://pyquil.readthedocs.io/en/latest/qpu.html
input_file = '19Q-Acorn.json'
options = {'org':'Rigetti'}
HG = Hardware_load(input_file, options)
adj_list = HG.adjacency_list
subgraph_size = 7 # for 7 qubits in the qneuron circuit

# Collect qubit labels
qubit_labels = []
for u,v in adj_list:
        if u not in qubit_labels:
                qubit_labels.append(u)
        if v not in qubit_labels:
                qubit_labels.append(v)

# Function for returning neighbors of a qubit
def neighbors(qubit_label):
	return set([y for x,y in adj_list if x==qubit_label] +\
		   [y for y,x in adj_list if x==qubit_label])

# Objective function to be fed into SA subroutine
def obj_func(input_mapping):
	res = check_compilation(inputs=input_mapping[0:2],\
				training=input_mapping[2],\
				ancilla=input_mapping[3:6],\
				output=input_mapping[6])
	return res.topological_swaps()+res.gate_depth()

# Function for generating a connected subgraph of the hardware given a starting
# node
def connected_subgraph_gen(node_start):

	# Perform depth first search for the same number of steps as the
	# number of qubits in the quantum circuit
	qubits_visited = []
	qubits_not_visited = deepcopy(qubit_labels)

	def dfs(q):
		if dfs.counter_total < dfs.counter_max:
			qubits_visited.append(q)
			qubits_not_visited.remove(q)
			dfs.counter_total = dfs.counter_total + 1
			for p in [x for x in neighbors(q)\
				  if x in qubits_not_visited]:
				dfs(p)
	dfs.counter_total = 0
	dfs.counter_max = subgraph_size
	dfs(node_start)

	return qubits_visited

def init_gen(): # choose a random initial node

	# Randomly choose a qubit
	rand_index = randint(0,len(qubit_labels)-1)
	qubit_chosen = qubit_labels[rand_index]

	return connected_subgraph_gen(qubit_chosen)

# Function for perturbing a particular connected subgraph of the hardware
def perturb_subgraph(qubit_list):

	eta = uniform(0,1)
	if eta > 0.5:
		# Generate a connected subgraph from a random node on the
		# current subgraph
        	rand_index = randint(0,len(qubit_list)-1)
        	qubit_chosen = qubit_list[rand_index]
		output_list = connected_subgraph_gen(qubit_chosen)
	else:
		# Shuffle the qubit labels in the current subgraph
		output_list = deepcopy(qubit_list)
		shuffle(output_list)
	return output_list

# Perturbation schemes which shift the subgraph multiple times 
# (psx for x times)
def ps2(qubit_list):
	out = qubit_list
	for i in range(0,2):
		out = perturb_subgraph(out)
	return out

def ps3(qubit_list):
        out = qubit_list
        for i in range(0,3):
                out = perturb_subgraph(out)
        return out

def ps4(qubit_list):
        out = qubit_list
        for i in range(0,4):
                out = perturb_subgraph(out)
        return out

# Optimize the objective function by simulated annealing
default_options = {
	'init_T': 10,
	'time_const': 25,
	'step_perT': 10,
	'final_T': 0.1,
	'maxiter': 2000,
	'perturb': perturb_subgraph,
}

def sa(init_guess, obj_function, options = default_options):
	"""
	Args:
		init_guess: initial guess for the qubit mapping.
		obj_function: Objective function
		options: a dictionary containing optimization settings.
			'init_T': initial temperature
			'time_const': time constant
			'step_perT': iterations per temperature
			'final_T': final temperature
				The overall annealing has temperature dropping
				as T0 * exp(-t/tau) where T0 is the initial
				temperature and tau is the time constant. Here
				the time parameter t is an integer marking the
				number of steps in dropping temperature so far. 				For every 'step_perT' number of iterations we 
				increment t by 1. Iterations are stopped until
				final temperature is reached or maximum number
				of iterations is reached.
			'maxiter': maximum number of iterations
			'perturb': function for perturbing the current guess
	Returns:
		results: a dictionary containing the outcome of optimization
			'fval_opt': optimized function value
			'xval_opt': optimized input
			'total_iter': total number of iterations
	"""

	# General simulated annealing parameters
	iter_count = 0
	iter_max = options['maxiter']
	xval_current = init_guess
	fval_current = obj_function(init_guess)
	ps = options['perturb']

	# Annealing scheme parameters
	T0 = options['init_T']
	tau = options['time_const']
	inner_count = 0
	step_perT = options['step_perT']
	t = 0
	T_current = T0
	T_final = options['final_T']
	if T0*exp(-iter_max/(step_perT*tau)) > T_final:
		print('Warning: final temperature not reached even at maximum iteration.')

	# Storing the history
	history_xval = [xval_current]
	history_fval = [fval_current]
	xval_opt = xval_current
	fval_opt = fval_current

	print("Iter\tFval")
	while iter_count < iter_max and T_current > T_final:

		# Generate and evaluate new guess
		xval_proposed = ps(xval_current)
		try:
			fval_proposed = obj_function(xval_proposed)
			print("%d\t%d" % (iter_count, fval_proposed))	
			iter_count = iter_count + 1
			inner_count = inner_count + 1
		except (AttributeError, ValueError):
			#print("(Error from quilc received and handled)")
			fval_proposed = fval_current
		delta_f = fval_proposed - fval_current		

		# Metropolis step
		if inner_count == step_perT:
			t = t + 1
			T_current = T0 * exp(-t/tau)
			inner_count = 0
		eta = uniform(0,1)
		if eta < min(1,exp(-delta_f/T_current)):
			if fval_proposed < fval_current:
				xval_opt = xval_proposed
				fval_opt = fval_proposed
			xval_current = xval_proposed
			fval_current = fval_proposed
		history_xval = history_xval + [xval_current]
		history_fval = history_fval + [fval_current]
		
		result = {
			'fval_opt': fval_opt,
			'xval_opt': xval_opt,
			'total_iter': iter_count,
			'history_xval': history_xval,
			'history_fval': history_fval
		}
	return result

if __name__ == "__main__":
	init_guess = init_gen()
	res = sa(init_guess, obj_func)
