# a small quantum circuit emulator wirten in python using numpy
# does not intergrate noise and only have the mps method.

import numpy as np
import qgempy as qg


class MPS:
    ''' Class to hold the MPS data 
    setup n q-tensor and n-1 l-tensor
    set up order 0 - n array
    set error for svd '''
    def __init__(self, N = 1, error = 0.01):
      self.qbit   = [np.array([[[0,1]]]) for _ in range(N)]
      self.Lambda = [np.array([[1]]) for _ in range(N-1)]
      self.order  = np.array(range(0,N))
      self.N      = N
      self.error  = error


    def add_single_gate(self, qbit, gate):
      '''Function to add a gate to one qubit.
        qbit: the qubit to apply the gate to.
        gate: the gate to be added. Either a tensor or string. 
      '''
      indices = np.where(self.order == qbit)[0][0]
      if isinstance(gate, str):
            gate = qg.get_single_gate(gate)
      self.qbit[indices]= np.einsum('ikj,jm->ikm',self.qbit[indices],gate) #  old code wand to keep for now np.dot(gate, self.qbit[indices])

    def svd_2qubit(self,indices1, indices2, gb2):
        '''Function to perform svd on a 2 qbit tensor
        indices1: index of qbit 1.
        indices2: index of qbit 2.
        gb2: tensor '''
        U,S,V =np.linalg.svd(gb2)
        self.qbit[indices1] = np.array([[U[0][0][1]]])
        self.Lambda[indices1] = np.array([S[0][1]]) 
        self.qbit[indices2] = np.array([[U[0][1][0]]])
       

    def combine_two_qubits(self, indices1, indices2):
        '''Function to combine two qubits
        indices1: index of first qbit.
        indices2: index of second qbit.'''
        mid = np.einsum('ikj,kl->ijl',self.qbit[indices1],self.Lambda[indices1])
        out = np.einsum('ijl,lkm->ijkm',mid,self.qbit[indices2])
        return out
        #if len(self.Lambda[indices1]) == 1:
        #    return np.tensordot(np.tensordot(self.qbit[indices1],self.Lambda[indices1],0),self.qbit[indices2],0)
        #else:
        #    return np.tensordot(np.tensordot(self.qbit[indices1],self.Lambda[indices1],1),self.qbit[indices2],1) """
        

    def swap_qubits(self, indices1, indices2):
        '''Function to swap two qubits
        indices1: index of first qbit.
        indices2: index of second qbit.'''
        gate = qg.get_double_gate("SWAP")
        qb2 = self.combine_two_qubits(indices1, indices2)
        qb2 = np.einsum('iljk,mnlk->imnj',qb2,gate)
        self.svd_2qubit(indices1, indices2, qb2)
        hold = self.order[indices2]
        self.order[indices2] = self.order[indices1]
        self.order[indices1] = hold

    def add_double_gate(self, qbit1, qbit2, gate):
        '''Function to add a gate that effects two qubits
        qbit1: the qubit to apply the gate to.
        qbit2: the qubit to apply the gate to.
        gate: the gate to be added. Either a tensor or string. '''
        
        indices1 = np.where(self.order == qbit1)[0][0]
        indices2 = np.where(self.order == qbit2)[0][0]
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

        if isinstance(gate, str):
            gate = qg.get_double_gate(gate)
        
        qb2 = self.combine_two_qubits(indices1, indices2)
        qb2 = np.einsum('iljk,mnlk->imnj',qb2,gate)
        self.svd_2qubit(indices1, indices2, qb2)

    def reorder(self):
        '''Reoder the qubits to orginal order'''
        while np.all(np.diff(self.order) <= 0):
            for i in range(self.N):
                place = np.where(self.order == i)[0][0]
                if place != i:
                    if place > i:
                        for j in range(place,i+1, -1):
                            self.swap_qubits(j-1, j)
                    else:
                        for j in range(place,i):
                            self.swap_qubits(j, j+1)
                    
    def creat_tensor_index(self, tensorIndexes, indices):
        '''Creates indices for tensor contraction.
        tensorIndexes: current tensaor indexes for large Tensor.
        indices: qbit number.
        '''
        indexContract = tensorIndexes[indices]
        nextChar = chr(ord(tensorIndexes[-1])+1)
        lambdaContract = tensorIndexes + ',' + indexContract + nextChar + '->'
        reducedTens = tensorIndexes.replace(tensorIndexes[indices], '') + nextChar 
        lambdaContract = lambdaContract + reducedTens
        nextQbit = reducedTens[-1] + chr(ord(nextChar)+1) + chr(ord(nextChar)+2)
        outTensor = reducedTens[:-1] + nextQbit[1:]
        qubitContract = reducedTens + ',' + nextQbit + '->' + outTensor
        return lambdaContract, qubitContract, outTensor 

    def contract_two_qubits(self, runingTensor, tensorIndexes, indices):
        '''Function to combine two qubits
        runingTensor: tensor to be contracted into.
        tensorIndexes: indexes for runingTensor.
        indices: qbit to be contracted with.
        '''
        lambdaContract, qubitContract, outTensor = self.creat_tensor_index(tensorIndexes, indices)
        mid = np.einsum(lambdaContract,runingTensor,self.Lambda[indices-1])
        return np.einsum(qubitContract,mid,self.qbit[indices]), outTensor


    def contract(self):
        '''Contracts the network.'''
        self.reorder
        out = self.qbit[0]
        tensorIndexes = 'abc'
        for i in range(1,self.N):
            out, tensorIndexes = self.contract_two_qubits(out,tensorIndexes, i)
        return out

        
        