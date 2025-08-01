# a small quantum circuit emulator wirten in python using numpy
# does not intergrate noise and only have the mps method.

import numpy as np
import qgempy as qg


class MPS:
    # Class to hold the MPS data 
    # setup n q-tensor and n-1 l-tensor
    # set up order 0 - n array
    # set error for svd
    def __init__(self, N = 1, error = 0.01):
      self.qbit   = [np.array([0,1]) for _ in range(N)]
      self.Lambda = [np.array([1]) for _ in range(N)]
      self.order  = np.array(range(0,N))
      self.N      = N
      self.error  = error


    def add_single_gate(self, qbit, gate):
      # function to add a gate to one qubit.
      indices = np.where(self.order == qbit)
      if gate.isstring:
            gate = qg.get_single_gate(gate)
      sedlf.qbit[indices]= np.dot(gate, self.qbit[indices])

    def svd_2qubit(self,indices1, indices2, gb2):
        #function to perform svd on a 2 qbit tensor
        U,S,V =np.linalg.svd(gb2 , full_matrices=False)
        self.qbit[indices1] = U[:,0] 
        self.Lambda[indices1] = S[0] 
        self.qbit[indices2] = V[0,:]

    def combine_two_qubits(self, indices1, indices2):
        #function to combine two qubits
        if len(self.Lambda[indices1]) == 1:
            return np.tensordot(np.tensordot(self.qbit[indices1],self.Lambda[indices1],0),self.qbit[indices2],0)
        else:
            return np.tensordot(np.tensordot(self.qbit[indices1],self.Lambda[indices1],1),self.qbit[indices2],1)
        
       

    def swap_qubits(self, indices1, indices2):
        #function to swap two qubits
        gate = qg.get_double_gate("SWAP")
        gb2 = self.combine_two_qubits(indices1, indices2)
        qb2 = np.dot(gate, qb2)
        self.svd_2qubit(indices1, indices2, gb2)
        hold = self.order[indices2]
        self.order[indices2] = self.order[indices1]
        self.order[indices1] = hold

    def add_double_gate(self, qbit1, qbit2, gate):
        #function to add a gate that effects two qubits
        indices1 = np.where(self.order == qbit1)
        indices2 = np.where(self.order == qbit2)
        if abs(indices1 - indices2) > 1:
            swapindices = min(indices1, indices2)
            finalindices = max(indices1, indices2)
            while swapindices < finalindices-1:
                self.swap_qubits(swapindices, swapindices + 1)
                swapindices += 1
            if self.order[swapindices] == qbit1:
                indices1 = swapindices
                indices2 = finalindices
            else:
                self.swap_qubits(swapindices, finalindices)
                indices1 = swapindices
                indices2 = finalindices
        if indices1 > indices2:
            self.swap_qubits(indices2, indices1)

        if gate.isstring:
            gate = qg.get_double_gate(gate)

        qb2 = self.combine_two_qubits(indices1, indices2)
        qb2 = np.dot(gate, qb2)
        self.svd_2qubit(indices1, indices2, gb2)

    def reorder(self):
        #reoder the qubits to orginal order
        while np.all(np.diff(self.order) <= 0):
            for i in range(len(self.N)):
                place = np.where(self.order == i)
                if place != i:
                    if place > i:
                        start = i
                        end   = place
                    else:
                        start = place
                        end   = i
                    for j in range(start,end):
                        self.swap(j, j+1)
                

    def comtract_two_qubits(self, runingTensor, indices):
        #function to combine two qubits
        if len(self.Lambda[indices1]) == 1:
            return np.tensordot(np.tensordot(runingTensor,self.Lambda[indices-1],0),self.qbit[indices],0)
        else:
            return np.tensordot(np.tensordot(runingTensor,self.Lambda[indices-1],1),self.qbit[indices],1)


    def contract(self):
        self.reorder
        out = self.qbit[0]
        for i in range(1,self.N):
            out = comtract_two_qubits(out, i)
        return out

        
        