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
        if (D[row][f_index] == 0 and Y[row] == 0):
            local_n0 += 1
        if (D[row][f_index] == 0 and Y[row] == 1):
            local_p0 += 1
        if (D[row][f_index] == 1 and Y[row] == 0):
            local_n1 += 1
        if (D[row][f_index] == 1 and Y[row] == 1):
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
        print("feautres_index", features_index)
        gains_list.append(calcGain_aux(features_index, D, Y, p, n, initial_entropy))
    return gains_list

def getPN(Y):
    p = n = 0
    for value in Y:
        if (value == 0):
            p += 1
        else:
            n += 1
    return (p, n)

def createdecisiontree_aux(D, Y, f):
    resTuple = getPN(Y)
    p = resTuple[0]
    n = resTuple[1]
    gains_and_favcases = calcGain(D, Y, p, n, entropy(p, n))
    gains = list(list(zip(*gains_and_favcases))[0])
    favcases = list(list(zip(*gains_and_favcases))[1])
    Y1 = []
    D1 = []
    Y2 = []
    D2 = []
    print(D)
    print(Y)
    # print(max(gains))
    #print(gains_and_favcases)
    #print(gains)
    if max(gains) == 1:
        return [gains.index(max(gains)), complementar(favcases[gains.index(max(gains))]), favcases[gains.index(max(gains))]]
    
    elif len(set(gains)) == 1 and gains[0] == 0:
        index = 0
        if index == f:
            index += 1
        for i in range(len(D)):
            if (D[i][index] == 0):
                D1 += [D[i]]
                Y1.append(Y[i])
            else:
                D2 += [D[i]]
                Y2.append(Y[i])
        return [index, createdecisiontree_aux(D1, Y1, f), createdecisiontree_aux(D2, Y2, f)]
    
    else:
        index = gains.index(max(gains))
        if favcases[index] == 0:
            for i in range(len(D)):
                if (D[i][index] == 0):
                    D1 += [D[i]]
                    Y1.append(Y[i])
            return [index, createdecisiontree_aux(D1, Y1, f), favcases[index]]
        else:
            for i in range(len(D)):
                if (D[i][index] == 1):
                    Y1.append(Y[i])
                    D1 += [D[i]]
            print("chose: ", index)
            return [index, complementar(favcases[index]), createdecisiontree_aux(D1, Y1, f)]

def createdecisiontree(D, Y, noise):
    decision_tree = []
    p = np.count_nonzero(Y == 1)
    n = np.count_nonzero(Y == 0)
    initial_entropy = entropy(p, n)
    # Y = np.asarray(Y)
    # D = np.asarray(D)
    # Y = Y.tolist()
    D = D.tolist()
    f = -1
    print(createdecisiontree_aux(D, Y, f))

if __name__ == "__main__":
    #D = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    #Y = [0, 0, 0, 1]
    D = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
    Y = [0, 1, 1, 0, 0, 1, 1, 0]
    createdecisiontree(D, Y, False)