# -*- coding: utf-8 -*-
"""
Grupo al059
Student id #92509
Student id #92427
"""

import numpy as np
import random

def entropy(p, n):
    if p == 0 or n == 0:
        return 0
    true_value = (-p / (n + p)) * np.log2(p / (n + p)) - (n / (n + p)) * np.log2(n / (n + p))
    if true_value < 0:
        return 0
    return true_value

def complementar(f):
    if f == 0:
        return 1
    return 0

def calcGain_aux(f_index, D, Y, p, n, initial_entropy):
    local_n0 = local_p0 = local_n1 = local_p1 = local_entropy_0 = local_entropy_1 = 0
    for row in range(len(Y)):
        if (D[row][f_index] == 0 and Y[f_index] == 0):
            local_n0 += 1
        if (D[row][f_index] == 0 and Y[f_index] == 1):
            local_p0 += 1
        if (D[row][f_index] == 1 and Y[f_index] == 0):
            local_n1 += 1
        if (D[row][f_index] == 1 and Y[f_index] == 1):
            local_p1 += 1
        local_entropy_0 = entropy(local_p0, local_n0)
        local_entropy_1 = entropy(local_p1, local_n1)

        if (local_entropy_0 > local_entropy_1):
            fav_case = 0
        else:
            fav_case = 1

        leftovers = ((local_p0 + local_n0) / (p + n)) * local_entropy_0 + ((local_p1 + local_n1) / (p + n)) * local_entropy_1
        gain = initial_entropy - leftovers
    return [gain, fav_case]

def calcGain(D, Y, p, n, initial_entropy):
    gains_list = []
    for features_index in range(len(D[0])):
        gains_list.append(calcGain_aux(features_index, D, Y, p, n, initial_entropy))
    return gains_list

def createdecisiontree_aux(D, Y, p, n, initial_entropy):
    gains_and_favcases = calcGain(D, Y, p, n, initial_entropy)
    gains = list(list(zip(*gains_and_favcases))[0])
    favcases = list(list(zip(*gains_and_favcases))[1])
    if max(gains) == 1:
        return [gains.index(max(gains)), complementar(favcases[gains.index(max(gains))]), favcases[gains.index(max(gains))]]
    
    elif len(set(gains)) == 1 and gains[0] == 0:
        index = random.randrange(0, len(gains) - 1)
        D = np.delete(D, index, axis = 1)
        for i in range(len(D)):
            if (D[i][index] != 0):
                D1 = np.delete(D, i, axis = 0)
                Y1 = np.delete(Y, i, axis = 0)
        for i in range(len(D)):
            if (D[i][index] != 1):
                D2 = np.delete(D, i, axis = 0)
                Y2 = np.delete(Y, i, axis = 0)
        return [index, createdecisiontree_aux(D1, Y1, p, n, initial_entropy), createdecisiontree_aux(D2, Y2, p, n, initial_entropy)]
    
    else:
        index = gains.index(max(gains))
        D = np.delete(D, index, axis = 1)
        if favcases[index] == 0:
            for i in range(len(D)):
                if (D[i][index] != 0):
                    D = np.delete(D, i, axis = 0)
                    Y = np.delete(Y, i, axis = 0)
            return [gains.index(max(gains)), createdecisiontree_aux(D, Y, p, n, initial_entropy), favcases[gains.index(max(gains))]]
        else:
            for i in range(len(D)):
                if (D[i][index] != 1):
                    D = np.delete(D, i, axis = 0)
                    Y = np.delete(Y, i, axis = 0)
            return [gains.index(max(gains)), complementar(favcases[gains.index(max(gains))]), createdecisiontree_aux(D, Y, p, n, initial_entropy)]

def createdecisiontree(D, Y, noise):
     decision_tree = []
     p = np.count_nonzero(Y == 1)
     n = np.count_nonzero(Y == 0)
     initial_entropy = entropy(p, n)
     print(createdecisiontree_aux(D, Y, p, n, initial_entropy))

if __name__ == "__main__":
     D = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
     Y = np.array([0, 0, 0, 1])
     #D = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
     #Y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
     createdecisiontree(D, Y, False)