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

def calcGains(D, Y, initial_entropy, gains, p, n, decision_tree, fav_case, calculated_attributes):
    for i in range(len(D[0])):
        local_ni0 = local_pi0 = local_ni1 = local_pi1 = local_entropy_i0 = local_entropy_i1 = 0
        if (i in calculated_attributes):
            gains.append(0) 
            continue
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

        print(local_entropy_i0, local_entropy_i1)

        if (local_entropy_i0 > local_entropy_i1):
            fav_case.append(0)
        else:
            fav_case.append(1)

        leftovers = ((local_pi0 + local_ni0) / (p + n)) * local_entropy_i0 + ((local_pi1 + local_ni1) / (p + n)) * local_entropy_i1
        gain = initial_entropy - leftovers
        gains.append(gain)
        print("gains ", gains)
    return (gains.index(max(gains)), fav_case[i], local_entropy_i0, local_entropy_i1, max(gains))

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
    calculated_attributes = []
    global_dict = {}
    while 1:
        # print("size: ", np.size(D[0]))
        max_gains_info = calcGains(D, Y, initial_entropy, gains, p, n, decision_tree, fav_case, calculated_attributes)
        max_gain_index = max_gains_info[0]
        print("max gain index: ", max_gain_index)
        print("max gain info 1", max_gains_info[1])
        if (max_gains_info[4] == 0):
            num_lines = len(D)
            print("primeiro if: ", num_lines)
            for i in range(num_lines-1):
                if (D[i][max_gain_index] != max_gains_info[1]):
                    D = np.delete(D, i, axis = 0)
                    print("oi", D)
                    num_lines = len(D)
            # break
        calculated_attributes.append(max_gain_index)
        #saving in dict favorable case and entropy values for attribute with bigger gain
        global_dict[max_gain_index] = (max_gains_info[1], max_gains_info[2], max_gains_info[3])
        index_order.append(max_gain_index)
        num_lines = len(D)
        for i in range(num_lines-1):
            print("segundo if: ", num_lines)
            if (D[i][max_gain_index] != max_gains_info[1]):
                D = np.delete(D, i, axis = 0)
                num_lines = len(D)
        print(D)
        gains = []
    print(global_dict)

if __name__ == "__main__":
    #D = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    #Y = np.array([0, 0, 0, 1])
    D = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
    Y = np.array([0, 1, 1, 0, 0, 1, 1, 0])
    createdecisiontree(D, Y, False)