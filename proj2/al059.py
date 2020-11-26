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

def calcGains(D, Y, initial_entropy, gains, p, n, decision_tree, fav_case):
    local_ni0 = local_pi0 = local_ni1 = local_pi1 = 0
    for i in range(len(D[0])):
        instances = D[:, i]
        for j in range (len(instances)):
            if (instances[j] == 0 and Y[j] == 0):
                local_ni0 += 1
            if (instances[j] == 0 and Y[j] == 1):
                local_pi0 += 1
            if (instances[j] == 1 and Y[j] == 0):
                local_ni1 += 1
            if (instances[j] == 1 and Y[j] == 1):
                local_pi1 += 1
        local_entropy_i0 = entropy(local_pi0, local_ni0)
        local_entropy_i1 = entropy(local_pi1, local_ni1)

        if (local_entropy_i0 > local_entropy_i1):
            fav_case.append(0)
        else:
            fav_case.append(1)

        leftovers = ((local_pi0 + local_ni0) / (p + n)) * local_entropy_i0 + ((local_pi1 + local_ni1) / (p + n)) * local_entropy_i1
        gain = initial_entropy - leftovers
        print("leftover:")
        print(leftovers)
        gains.append(gain)
        print(gains)
    return (gains.index(max(gains)), fav_case[i], local_entropy_i0, local_entropy_i1)

def createdecisiontree(D, Y, noise = False):
    #init tree
    decision_tree = []
    #save p and n
    p = np.count_nonzero(Y == 1)
    n = np.count_nonzero(Y == 0)
    #initial entropy
    initial_entropy = entropy(p, n)
    #for each col calculate respective entropy, leftovers, no pain no gain
    gains = []
    index_order = []
    fav_case = []
    global_dict = {}
    while np.size(D):
        max_gains_info = calcGains(D, Y, initial_entropy, gains, p, n, decision_tree, fav_case)
        max_gain_index = max_gains_info[0]
        #saving in dict favorable case and entropy values for attribute with bigger gain
        print(max_gain_index)
        global_dict[max_gain_index] = (max_gains_info[1], max_gains_info[2], max_gains_info[3])
        index_order.append(max_gain_index)
        print(D)
        D = np.delete(D, max_gain_index, axis = 0)
        print(D)
        gains = []
    print(global_dict)

if __name__ == "__main__":
    #D = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    #Y = np.array([0, 0, 0, 1])
    D = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
    Y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
    createdecisiontree(D, Y, False)