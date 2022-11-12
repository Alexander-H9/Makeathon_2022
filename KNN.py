#!/usr/bin/env python
# coding: utf-8

import numpy as np

# 200 - 100 - 50 - 20 - 10 - 5 - 2 - 1
X = np.array([[202, 155, 645, 170],     # 2 €
                [220, 195, 394, 142],   # 1 €
                [657, 625, 675, 135],   # 50 Cent
                [610, 618, 646, 122],   # 20 Cent
                [607, 621, 655, 106],   # 10 Cent
                [378, 347, 415, 650],   # 5 Cent
                [420, 440, 468, 540],   # 2 Cent
                [608, 634, 619, 400],   # 1 Cent
            ])

def prep_data(data):
    """
    Prepare Data
    """
    length = len(data)
    end_first_third = length//3
    end_second_third = int(length//1.5)

    min_left = min(data[0:end_first_third])
    min_right = min(data[end_second_third:length])
    max_m = max(data[end_first_third:end_second_third])

    return np.array([min_left, min_right, max_m, length]).tolist()

def get_k_nearest_neighbors(data_vector,data_martrix,k=1):
    """
    compute the k nearest neighbors for a query vector x given a data matrix X
    :param x: the query vector x
    :param X: the N x D data matrix (in each row there is data vector) as a numpy array
    :param k: number of nearest-neighbors to be returned
    :return: return list of k line indixes referring to the k nearest neighbors of x in X
    """
    distances = [np.linalg.norm(data_martrix[i]-data_vector) for i in range(len(data_martrix))]
    return np.argsort(distances)[:k]
