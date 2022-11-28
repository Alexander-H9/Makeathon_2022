import numpy as np

def prep_data(data):
    """
    Prepare Data. Use this function for the prediction of the measurement
    """
    length = len(data)
    end_first_third = length//3
    end_second_third = int(length//1.5)

    min_left = min(data[0:end_first_third])
    min_right = min(data[end_second_third:length])
    max_m = max(data[end_first_third:end_second_third])

    return np.array([min_left, min_right, max_m, length]).tolist()


def prep_data_list(data):
    """
    Prepare the raw data from the database. Use this function to create a model
    """
    res = []
    for coin in data:
        length = len(coin)
        end_first_third = length//3
        end_second_third = int(length//1.5)
        min_left = min(coin[0:end_first_third])
        min_right = min(coin[end_second_third:length])
        max_m = max(coin[end_first_third:end_second_third])

        res.append([min_left, min_right, max_m, length])

    return res


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
