#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from qiskit.tools.visualization import plot_histogram

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Kraus, SuperOp
from qiskit.providers.aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)

import numpy as np

qc = QuantumCircuit(9,4)
qc.h([5,6,7,8])

qc.cx(5,0)
qc.cx(5,1)
qc.cx(5,2)
qc.cx(6,2)
qc.cx(6,3)
qc.cx(6,4)
qc.cz(7,0)
qc.cz(7,2)
qc.cz(7,3)
qc.cz(8,1)
qc.cz(8,2)
qc.cz(8,4)

qc.h([5,6,7,8])
qc.measure([5,6,7,8],[3,2,1,0])

#qc.draw()

file = open("512.txt","w")
c1=0
    
for w in range(100):
    sim = AerSimulator()  # make new simulator object
    noise_bit_flip = NoiseModel()
    sim_noise = AerSimulator(noise_model=noise_bit_flip)
    job = sim.run(qc)      # run the experiment
    result = job.result()  # get the results
    result.get_counts()    # interpret the results as a "counts" dictionary

    result_ideal = sim.run(qc).result()
    #plot_histogram(result_ideal.get_counts(0))

    p=(w+1)/1000
    #p=0.01
    p_reset = p
    p_meas = p
    p_gate1 = p
    p_gate3 = p
    p_depol = p

    error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])
    error_reset2 = pauli_error([('Z', p_reset), ('I', 1 - p_reset)])

    error_depol = depolarizing_error(p_depol, 1) #single-qubit error
    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_meas2 = pauli_error([('Z',p_meas), ('I', 1 - p_meas)])
    error_gate1 = pauli_error([('X',p_gate1), ('I', 1 - p_gate1)])
    error_gate1 = pauli_error([('Z',p_gate1), ('I', 1 - p_gate1)])
    error_gate2 = error_gate1.tensor(error_gate1)
    
    noise_bit_flip.add_all_qubit_quantum_error(error_reset, "reset")
    noise_bit_flip.add_all_qubit_quantum_error(error_reset2, "reset2")
    #noise_bit_flip.add_all_qubit_quantum_error(error_depol, "depolarizing")
    #noise_bit_flip.add_all_qubit_quantum_error(error_meas, "measure")
    #noise_bit_flip.add_all_qubit_quantum_error(error_meas2, "measure")
    #noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
    noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cz"])
    noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cx"])

    
    qc_tnoise = transpile(qc, sim_noise)

    result_bit_flip = sim_noise.run(qc_tnoise).result()
    counts_bit_flip = result_bit_flip.get_counts(0)
    c=0
    for q,d in counts_bit_flip.items():
        if d>=100:
            c+=d
            c1+=d
    #print("p = ",p,"prob = ",c/1024)
    #print(counts_bit_flip)
    # Plot noisy output
    #plot_histogram(counts_bit_flip)

    print("p = ",p,"prob = ",c/1024)
    
    cnt.append(c/1024)
np.savetxt(file,cnt,fmt='%1.10f')


# In[ ]:




