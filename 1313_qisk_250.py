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


file = open("1313.txt","w")
qc = QuantumCircuit(25,12)
qc.h([13,14,15,16,17,18,19,20,21,22,23,24])

qc.cx(13,0)
qc.cx(13,1)
qc.cx(13,3)
qc.cx(14,1)
qc.cx(14,2)
qc.cx(14,4)
qc.cx(15,3)
qc.cx(15,5)
qc.cx(15,6)
qc.cx(15,8)
qc.cx(16,4)
qc.cx(16,6)
qc.cx(16,7)
qc.cx(16,9)
qc.cx(17,8)
qc.cx(17,10)
qc.cx(17,11)
qc.cx(18,9)
qc.cx(18,11)
qc.cx(18,12)

qc.cz(19,0)
qc.cz(19,3)
qc.cz(19,5)
qc.cz(20,1)
qc.cz(20,3)
qc.cz(20,4)
qc.cz(20,6)
qc.cz(21,2)
qc.cz(21,4)
qc.cz(21,7)
qc.cz(22,5)
qc.cz(22,8)
qc.cz(22,10)
qc.cz(23,6)
qc.cz(23,8)
qc.cz(23,9)
qc.cz(23,11)
qc.cz(24,7)
qc.cz(24,9)
qc.cz(24,12)

qc.h([13,14,15,16,17,18,19,20,21,22,23,24])
qc.measure([13,14,15,16,17,18,19,20,21,22,23,24],[11,10,9,8,7,6,5,4,3,2,1,0])


c1=0
cnt=[]
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
    noise_bit_flip.add_all_qubit_quantum_error(error_depol, "depolarizing")
    noise_bit_flip.add_all_qubit_quantum_error(error_meas, "measure")
    #noise_bit_flip.add_all_qubit_quantum_error(error_meas2, "measure")
    #noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
    noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cz"])
    noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cx"])


    qc_tnoise = transpile(qc, sim_noise)

    result_bit_flip = sim_noise.run(qc_tnoise).result()
    counts_bit_flip = result_bit_flip.get_counts(0)
    c=0
    for q,d in counts_bit_flip.items():
        if d>=4:
            c+=d
            c1+=d
    #print("p = ",p,"prob = ",c/1024)
    #print(counts_bit_flip)
    # Plot noisy output
    #plot_histogram(counts_bit_flip)

    print(c/1024)
    cnt.append(c/1024)
np.savetxt(file,cnt,fmt='%1.10f')

