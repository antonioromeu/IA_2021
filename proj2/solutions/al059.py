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
    true_value = (-p / (n + p)) * np.log2(p / (n + p)) - (n / (n + p)) * np.log2(n / (n + p))
    if true_value < 0:
        return 0
    return true_value

def complementar(f):
    if f == 0:
        return 1
    return 0

def getPN(Y):
    p = n = 0
    for value in Y:
        if (value == 0):
            p += 1
        else:
            n += 1
    return (p, n)

def getMajority(D, Y):
    c0 = c1 = 0
    for i in range(len(D)):
        for j in range(len(D[i])):
            if D[i][j] == 0 and Y[i] == 1:
                c0 += 1
            elif D[i][j] == 1 and Y[i] == 1:
                c1 += 1
    return max(c0, c1)

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
    leftovers = ((local_p0 + local_n0) / (p + n)) * local_entropy_0 + ((local_p1 + local_n1) / (p + n)) * local_entropy_1
    gain = initial_entropy - leftovers
    return [gain, local_entropy_0, local_entropy_1]

def calcGain(D, Y, p, n, initial_entropy):
    gains_list = []
    for features_index in range(len(D[0])):
        gains_list.append(calcGain_aux(features_index, D, Y, p, n, initial_entropy))
    return gains_list

def createdecisiontree_aux(D, Y, f_index, noise):
    # print(Y)
    resTuple = getPN(Y)
    p = resTuple[0]
    n = resTuple[1]
    gains_and_favcases = calcGain(D, Y, p, n, entropy(p, n))
    gains = list(list(zip(*gains_and_favcases))[0])
    li0 = list(list(zip(*gains_and_favcases))[1])
    li1 = list(list(zip(*gains_and_favcases))[2])
    Y1 = []
    D1 = []
    Y2 = []
    D2 = []

    if (Y == [] or D == []):
        return

    if all(v == 0 for v in Y):
        return 0
    elif all(v == 1 for v in Y):
        return 1
    
    elif (noise == False and (max(gains) == 0 or len(gains) != len(set(gains)))) or (noise == True and max(gains) == 0):
        if f_index == len(D[0]) - 1:
            print("fghjk")
            return getMajority(D, Y)
        if (max(gains) == 0):
            f_index += 1
        else:
            f_index = gains.index(max(gains))
        for i in range(len(D)):
            if D[i][f_index] == 0:
                D1 += [D[i]]
                Y1 += [Y[i]]
            else:
                D2 += [D[i]]
                Y2 += [Y[i]]

        if (D1 == [] or D2 == []):
            return getMajority(D, Y)
        c1 = createdecisiontree_aux(D1, Y1, f_index, noise)
        c2 = createdecisiontree_aux(D2, Y2, f_index, noise)
        if (c1 == c2):
            return c1
        return [f_index, c1, c2]
        
    elif max(gains) == 1:
        f_index = gains.index(max(gains))
        if D[0][f_index] == 0:
            return [f_index, Y[0], complementar(Y[0])]
        return [f_index, complementar(Y[0]), Y[0]]
    
    #arvore começa no fav case
    else:
        f_index = gains.index(max(gains))
        for i in range(len(D)):
            if D[i][f_index] == 0:
                D1 += [D[i]]
                Y1 += [Y[i]]
            else:
                D2 += [D[i]]
                Y2 += [Y[i]]
        
        c1 = createdecisiontree_aux(D1, Y1, f_index, noise)
        c2 = createdecisiontree_aux(D2, Y2, f_index, noise)

        if (li0[f_index] == 0 and li1[f_index] == 0):
            if D[0][f_index] == 0:
                return [f_index, Y[0], complementar(Y[0])]
            return [f_index, complementar(Y[0]), Y[0]]

        if li0[f_index] == 0:
            for i in range(len(D)):
                if D[i][f_index] == 0:
                    return [f_index, Y[i], c2]
         
        elif li1[f_index] == 0:
            for i in range(len(D)):
                if D[i][f_index] == 1:
                    return [f_index, c1, Y[i]]
        
        else:
            if c1[1] == c2[1] and c1[0] == c2[0]:
                return [c1[0], c1[1], [f_index, c1[2], c2[2]]]
            return [f_index, c1, c2]

def createdecisiontree(D, Y, noise):
    decision_tree = []
    p = np.count_nonzero(Y == 1)
    n = np.count_nonzero(Y == 0)
    D = D.astype(int)
    D = D.tolist()
    Y = Y.astype(int)
    Y = Y.tolist()

    if (noise == 0.1):
        true_noise = True
    else:
        true_noise = False


    if (all(v == 0 for v in Y)):
        return [0, 0, 0]
    elif (all(v == 1 for v in Y)):
        return [0, 1, 1]

    if (true_noise == True):
        print(createdecisiontree_aux(D, Y, -1, true_noise))

    return createdecisiontree_aux(D, Y, -1, true_noise)

# if __name__ == "__main__":
#     #D = np.array([[False, False], [False, True], [True, False], [True, True]])
#     #Y = np.array([False, False, False, True])
#     #D = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
#     #Y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
#     #D = np.array([[0,0],[0,1],[1,0],[1,1]])
#     #Y = np.array([1, 1, 1, 0])
#     #D = np.array([[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]])
#     #Y = np.array([1, 0, 0, 1, 0, 1, 0, 1])
#     # Y = np.array([0, 1, 0, 1, 0, 1, 0, 1])
#     np.random.seed(13102020)
#     D = np.random.rand(1000,10)>0.5
#     Y = ((D[:,1] == 0) & (D[:,6] == 0)) | ((D[:,3] == 1) & (D[:,4] == 1))  
#     print(createdecisiontree(D, Y, False))