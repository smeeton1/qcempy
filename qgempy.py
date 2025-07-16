# This contains the functions to generate the arrays for gates.

import numpy as np


def get_single_gate(s):
    match s:
        case "X":
            return np.array([[0, 1], [1, 0]])
        case "Y":
            return np.array([[0, -1j], [1j, 0]])
        case "Z":
            return np.array([[1, 0], [0, -1]])
        case "H":
            return np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        case "S":
            return np.array([[1, 0], [0, 1j]])
        case "T":
            return np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
        case "I":
            return np.array([[1, 0], [0, 1]])
        case _:
            raise ValueError("Invalid gate")


def get_double_gate(s):
    match s:
        case "CX":
            return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
        case "CY":
            return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]])
        case "CZ":
            return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
        case "CH":
            return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, -1]]) / np.sqrt(2)
        case "CS":
            return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]])
        case "CT":
            return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(1j * np.pi / 4)]])
        case "CI":
            return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        case "SWAP":
            return np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
        case _:
            raise ValueError("Invalid gate")