#unit test for qcempy

import qcempy as qc
import qgempy as qg
import numpy as np
import pytest

def test_MPS():
    MPStest = qc.MPS(3)
    assert len(MPStest.qbit) ==3
    assert len(MPStest.Lambda) ==3
    assert len(MPStest.order) ==3
    assert (MPStest.qbit[0] == [0,1]).all()
    assert (MPStest.qbit[1] == [0,1]).all()
    assert (MPStest.qbit[2] == [0,1]).all()
    assert (MPStest.Lambda[0] == [1]).all()
    assert (MPStest.Lambda[1] == [1]).all()
    assert (MPStest.Lambda[2] == [1]).all()
    assert (MPStest.order[0] == [0]).all()
    assert (MPStest.order[1] == [1]).all()
    assert (MPStest.order[2] == [2]).all()
    assert MPStest.error == 0.01

def test_single_gate_get():
    assert (qg.get_single_gate('X') == np.array([[0, 1], [1, 0]])).all()
    assert (qg.get_single_gate('Y') == np.array([[0, -1j], [1j, 0]])).all()
    assert (qg.get_single_gate('Z') == np.array([[1, 0], [0, -1]])).all()
    assert (qg.get_single_gate('H') == np.array([[1, 1], [1, -1]])/np.sqrt(2)).all()
    assert (qg.get_single_gate('S') == np.array([[1, 0], [0, 1j]])).all()
    assert (qg.get_single_gate('T') == np.array([[1, 0], [0, np.exp(1j*np.pi/4)]])).all()
    assert (qg.get_single_gate('I') == np.array([[1, 0], [0, 1]])).all()

def test_double_gate_get():
    assert (qg.get_double_gate('CX') == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])).all()
    assert (qg.get_double_gate('CY') == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]])).all()
    assert (qg.get_double_gate('CZ') == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])).all()
    assert (qg.get_double_gate('CH') == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, -1]])/np.sqrt(2)).all()
    assert (qg.get_double_gate('CS') == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]])).all()
    assert (qg.get_double_gate('CT') == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(1j*np.pi/4)]])).all()
    assert (qg.get_double_gate('SWAP') == np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])).all()
    assert (qg.get_double_gate('CI') == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])).all()