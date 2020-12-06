# -*- coding: utf-8 -*-
"""
Grupo al059
Student id #92509
Student id #92427
"""
import numpy as np

def entropy(p, n):
    if p == 0 or n == 0:
        return 0
    return (-p / (n + p)) * np.log2(p / (n + p)) - (n / (n + p)) * np.log2(n / (n + p))

def complementar(f):
    return 1 - f

def getMajority(Y):
    c0 = Y.count(0)
    c1 = Y.count(1)
    if (c0 > c1):
        return 0
    elif (c1 > c0):
        return 1
    return -1

def cutTree(D, Y, f_index):
    D1 = []
    D2 = []
    Y1 = []
    Y2 = []
    for i in range(len(D)):
        if D[i][f_index] == 0:
            D1 += [D[i]]
            Y1 += [Y[i]]
        else:
            D2 += [D[i]]
            Y2 += [Y[i]]
    return (D1, Y1, D2, Y2)

def calcGain_aux(f_index, D, Y, p, n, initial_entropy):
    local_n0 = local_p0 = local_n1 = local_p1 = 0
    for row in range(len(Y)):
        if (D[row][f_index] == 0 and Y[row] == 0):
            local_n0 += 1
        elif (D[row][f_index] == 0 and Y[row] == 1):
            local_p0 += 1
        elif (D[row][f_index] == 1 and Y[row] == 0):
            local_n1 += 1
        else:
            local_p1 += 1
    local_entropy_0 = entropy(local_p0, local_n0)
    local_entropy_1 = entropy(local_p1, local_n1)
    leftovers = ((local_p0 + local_n0) / (p + n)) * local_entropy_0 + ((local_p1 + local_n1) / (p + n)) * local_entropy_1
    gain = initial_entropy - leftovers
    return [gain, local_entropy_0, local_entropy_1]

def calcGain(D, Y, p, n, initial_entropy):
    gains_list = []
    for features_index in range(len(D[0])):
        gains_list.append(calcGain_aux(features_index, D, Y, p, n, initial_entropy))
    return gains_list

def createdecisiontree_aux(D, Y, f_index, noise):
    p = Y.count(1)
    n = Y.count(0)
    gains_and_favcases = calcGain(D, Y, p, n, entropy(p, n))
    gains = list(list(zip(*gains_and_favcases))[0])
    li0 = list(list(zip(*gains_and_favcases))[1])
    li1 = list(list(zip(*gains_and_favcases))[2])

    #remaining examples are all negative
    if all(v == 0 for v in Y):
        return 0
    
    #remaining examples are all positive
    elif all(v == 1 for v in Y):
        return 1
    
    #maximum gain is 0 or there are repeated gain values (uncertainty)
    elif max(gains) == 0 or len(gains) != len(set(gains)):
        if max(gains) == 0:
            f_index += 1
            #no more attributes left (only happens if there's noise)
            if f_index == len(D[0]) and noise == True:
                #assuming 0 for majority vote unconclusive
                return 0 if getMajority(Y) == -1 else getMajority(Y)
        else:
            #choosing attribute w/ biggest gain
            f_index = gains.index(max(gains))
        
        t = cutTree(D, Y, f_index)
        D1 = t[0]
        Y1 = t[1]
        D2 = t[2]
        Y2 = t[3]
        
        #no examples left (solving with majority vote, assuming 1 for unconclusive)
        if noise == True and (D1 == [] or D2 == []):
            return 1 if getMajority(Y) == -1 else getMajority(Y)

        c1 = createdecisiontree_aux(D1, Y1, f_index, noise)
        c2 = createdecisiontree_aux(D2, Y2, f_index, noise)

        #shortening tree if left and right are the same, else expand tree
        return c1 if c1 == c2 else [f_index, c1, c2]

    #stopping case when maximum gain is 1
    elif max(gains) == 1:
        f_index = gains.index(max(gains))
        if D[0][f_index] == 0:
            return [f_index, Y[0], complementar(Y[0])]
        return [f_index, complementar(Y[0]), Y[0]]
    
    # 0 < maximum gain < 1
    else:
        f_index = gains.index(max(gains))
        t = cutTree(D, Y, f_index)
        D1 = t[0]
        Y1 = t[1]
        D2 = t[2]
        Y2 = t[3]

        c1 = createdecisiontree_aux(D1, Y1, f_index, noise)
        c2 = createdecisiontree_aux(D2, Y2, f_index, noise)

        #both of the attribute's values have entropy 0
        if (li0[f_index] == 0 and li1[f_index] == 0):
            if D[0][f_index] == 0:
                return [f_index, Y[0], complementar(Y[0])]
            return [f_index, complementar(Y[0]), Y[0]]

        #favorable case is 1
        if li0[f_index] == 0:
            for i in range(len(D)):
                if D[i][f_index] == 0:
                    return [f_index, Y[i], c2]
        
        #favorable case is 0
        elif li1[f_index] == 0:
            for i in range(len(D)):
                if D[i][f_index] == 1:
                    return [f_index, c1, Y[i]]
        
        #shortening tree if sons have the same head and left tree
        if (c1[0] == c2[0] and c1[1] == c2[1]):
            return [c1[0], c1[1], [f_index, c1[2], c2[2]]]
        
        #shortening tree if sons have the same head and right tree
        if (c1[0] == c2[0] and c1[2] == c2[2]):
            return [c1[0], [f_index, c1[1], c2[1]], c1[2]]
        
        #there is no favorable case
        return [f_index, c1, c2]

def createdecisiontree(D, Y, noise):
    p = np.count_nonzero(Y == 1)
    n = np.count_nonzero(Y == 0)
    D = (D.astype(int)).tolist()
    Y = (Y.astype(int)).tolist()
    true_noise = True if noise != 0 else False

    if all(v == 0 for v in Y):
        return [0, 0, 0]
    elif all(v == 1 for v in Y):
        return [0, 1, 1]

    return createdecisiontree_aux(D, Y, -1, true_noise)