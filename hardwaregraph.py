# Define the basic classes needed for hardware embedding

from numpy import zeros

class HardwareGraph():
	"""
	Base class for all hardware graphs. Here we assume there is a priori
	a defined ordering of all of the qubits from 0 to N-1, and all qubits
	are functional. Dead qubits will need to be excluded in a preprocessing
	step.
	"""
	def __init__(self, qubit_list, adjacency_list, fidelity_list):
		"""
		Instantiate a hardware graph object.

		Args:
			qubit_list: a list of integers each indexing a qubit in
					the abstract quantum circuit. The order
					of elements in this list is important
					because it directly corresponds to the
					entries in fidelity_list.
			adjacency_list: a list of tuples showing the graph of
					connectivity of the hardware. The order
					of tuples in this list is important
					because it directly corresponds to the
					way elements of lists in fidelity_list
					are ordered.
					e.g. the following shows a 4Q circuit 
					forming a square:
						[(0,1),(1,2),(2,3),(3,0)]
					and the two-qubit fidelity for each
					edge in fidelity_list will be stored as
					   e.g. [0.92, 0.87, 0.95, 0.99]
					with each entry corresponding to the
					element in this adjacency list.
			fidelity_list: a dictionary containing
				single_qubit: a dictionary which contains
						single qubit fidelity
						values associated with each
						qubit. The ordering follows
						that used in the adjacency list
				two_qubit: a dictionary which contains various 
						two-qubit fidelity values
						associated with each pair of
						connected qubits. The ordering
						follows that used in the 
						adjacency list.
		"""

		self.nqubits = len(qubit_list)
		self.qubit_list = qubit_list
		self.adjacency_list = adjacency_list
		self.fidelity_list = fidelity_list

def Hardware_load(input_file, options):
	"""
	Function for loading hardware information into a HardwareGraph object.
	
	Args:
		input_file: source of the hardware information. The data type
				of this parameter largely depends on the
				specific circumstance of the hardware as
				described in 'options'.
		options: a dictionary containing descriptors of the hardware.
			org: name of the organization which produces and
				maintains the hardware. Currently supported
				entries include the following manufacturers:
		
				'Rigetti': input_file is the name of a JSON
					file containing information about the
					hardware.
				'IBM'
				'Google'
	
	Returns:
		A HardwareGraph object.
	"""

	if options['org'] == 'Rigetti':

		# Extract information about Rigetti Quantum Processing Unit.
		# For details see
		#  http://pyquil.readthedocs.io/en/stable/qpu_overview.html

		# Read the device specification JSON file
		import json
		with open(input_file, 'r') as infile:
			dev_data = json.load(infile)
		dic_qubits = dev_data['isa']['1Q']
		dic_pairs = dev_data['isa']['2Q']
		dic_f1Q = dev_data['specs']['1Q'] # single-qubit fidelity
		dic_f2Q = dev_data['specs']['2Q'] # two-qubit fidelity

		list_qubit_keys = list(dic_qubits.keys())
		list_pair_keys = list(dic_pairs.keys())

		# Extract data from the dictionary
		qubit_list = []
		dead_list = []
		adjacency_list = []
		f1QRB = [] 	# Single-qubit error; randomized benchmarking
		f1RO = [] 	# Single-qubit read-out error
		f2CZ = [] 	# Two-qubit controlled-Z gate error
		f2CPHASE = [] 	# Two-qubit controlled-phase gate error	

		for key in list_qubit_keys: # Each key for one qubit
			if len(dic_qubits[key])==0: # if the qubit is not dead
				qubit_list.append(int(key))
				try:
					f1QRB.append(dic_f1Q[key]['f1QRB'])
					f1RO.append(dic_f1Q[key]['fRO'])
				except(KeyError):
					f1QRB.append(1)
					f1RO.append(1)
			else:
				if dic_qubits[key]['dead']=='true':
					dead_list.append(int(key))
		
		for key in list_pair_keys: # Each key for a pair
			qubit_labels = key.split("-")
			u = int(qubit_labels[0])
			v = int(qubit_labels[1])
			if u not in dead_list and v not in dead_list:
				adjacency_list.append((u,v))
				try:
					f2CZ.append(dic_f2Q[key]['fCZ'])
					f2CPHASE.append(dic_f2Q[key]['fCPHASE'])
				except(KeyError):
					f2CZ.append(1)
					f2CPHASE.append(1)

		# Assemble the data structure for a HardwareGraph object
		fidelity_list = {
			'single_qubit':{
				'f1QRB':f1QRB,
				'f1RO':f1RO
			},
			'two-qubit':{
				'f2CZ':f2CZ,
				'f2CPHASE':f2CPHASE
			}
		}
		output = HardwareGraph(qubit_list, adjacency_list,\
				fidelity_list)

	return output
