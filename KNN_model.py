import json
import numpy as np
from measurement import measurement as mes
from plot_graphs import plot_evaluation

class Model:
    """
    Class representing a Model
    """
    def __init__(self, model_type, model_from_db=None, name="default"):
        self.name: str = name
        self.model_type: str = model_type
        self.key_mapping = {0: "2€", 1: "1€", 2: "0.5€", 3: "0.20€",
                            4: "0.10", 5: "0.05€", 6: "0.02€", 7: "0.01€"}

        if model_from_db:
            self.model = model_from_db
            self.create_small_model_from_training_data()
        else:
            try:
                with open(f'models/{self.name}', 'r', encoding="utf-8") as j:
                    self.model: dict = json.loads(j.read())

            except FileNotFoundError:
                print("Creating a new model ", self.name)
                with open(f'models/{self.name}', 'w', encoding="utf-8") as j:
                    pass

                self.model: dict = {}
                self.write_model()


    def create_small_model_from_training_data(self):
        """
        Convert the large modell to the small
        """
        small_model: dict = {}

        for entry in self.model:
            self.model[entry] = prep_data_list(self.model[entry])
            small_model[entry] = [sum(x) for x in zip(*self.model[entry])]
            small_model[entry] = [int(x / len(self.model[entry])) for x in small_model[entry]]
            small_model[entry].append(len(self.model[entry]))

        self.model_type = "small"
        self.model = small_model


    def write_model(self):
        """
        Write the model to a json file
        """

        with open(f'models/{self.name}', 'w', encoding="utf-8") as j:
            j.write(json.dumps(self.model, indent=4))


    def update_model(self, coin: str, wight_update):
        """
        Update one coin weight
        """

        if self.model_type == "small":
            self.update_small_model(coin, wight_update) 
        if self.model_type == "large":
            self.update_large_model(coin, wight_update) 


    def update_small_model(self, coin: str, wight_update):
        """
        Update one coin weight for the small model
        """

        # if the model has no entry 
        if self.model.get(coin) is None:
            print(f"Add new entry for {coin} coins at model {self.name}")
            wight_update += (1,)
            self.model[coin] = (wight_update)
            self.write_model()
            return

        wights = self.model[coin][:-1]
        amount = self.model[coin][4]

        for idx,wight in enumerate(wights):

            wights[idx] = int(round((wight_update[idx]/amount + wight*((amount-1)/amount)), 0))

        amount += 1
        wights.append(amount)
        self.model[coin] = wights
        self.write_model()


    def update_large_model(self, coin: str, wight_update):
        """
        Update one coin wight for the large model
        """

        if self.model.get(coin) is None:
            print(f"Add new entry for {coin} coins at model {self.name}")
            self.model[coin] = [(wight_update)]
            self.write_model()
            return

        self.model[coin].append(list(wight_update))
        self.write_model()


    def predict(self, measurement, model_labels):
        """
        predict the measurement and returns the idx of the knn
        """
        if len(measurement) != 4:
            measurement = prep_data(measurement)

        np_matrix = np.array(list(self.model.values()))

        # remove the amount column which is only required to train the small model
        if self.model_type == "small":
            np_matrix = np.delete(np_matrix, 4, 1)

        idx_knn = get_k_nearest_neighbors(measurement, np_matrix, 1)

        if len(model_labels) < idx_knn[0]:
            print("ERROR Max, da läuft irgend was nicht ganz rund in der Datenbank")
            exit()

        return model_labels[idx_knn[0]]


    def evaluate_automatic(self, y, model_labels):
        """
        evaluate the model and returns the accuracy
        this function requires a specific construction which can loop the coin
        """

        ITERATIONS = 10
        true_prediction = 0

        for _ in range(ITERATIONS):

            measurement = mes()
            if len(measurement) != 4:
                measurement = prep_data(measurement)

            if self.predict(measurement, model_labels) == y:
                true_prediction += 1

        accuracy = round(true_prediction/ITERATIONS, 2)*100
        return accuracy


    def evaluate(self, labels:list):
        """
        evaluate the model and returns the accuracy
        """
        print(f'The following coins will be evaluated: {labels}\n')
        accuracy_coins = {}
        mean_accuracy_model = 0

        for label in labels:
            evaluate = True
            iteration = 1
            true_prediction = 0
            while evaluate:
                print(f'\nEvaluate {label}')
                measurement = mes()

                if self.predict(measurement, labels) == label:
                    true_prediction += 1
                    print("Prediction was True")

                else: print("Prediction was False")

                keep_going = input(f'Do you want to continue to evaluate {label}?\nIt has evaluated {iteration} times\nyes or no ?\n')

                if keep_going == "yes":
                    iteration += 1
                elif keep_going == "no":
                    accuracy_coins[str(label)] = round(true_prediction/iteration, 2)*100
                    mean_accuracy_model += accuracy_coins[str(label)]
                    print("current acc: ", accuracy_coins)
                    print("current model sum acc: ", mean_accuracy_model)
                    evaluate = False
                else:
                    print("Invalid user input, please confirm only with yes or no")
                    exit()

        mean_accuracy_model = round((mean_accuracy_model/len(labels)), 2)
        print("mean_accuracy_model: ", mean_accuracy_model)
        accuracy_coins["model"] = mean_accuracy_model

        return accuracy_coins


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


def get_k_nearest_neighbors(data_vector,data_matrix,k=1):
    """
    compute the k nearest neighbors for a query vector x given a data matrix X
    :param x: the query vector x
    :param X: the N x D data matrix (in each row there is data vector) as a numpy array
    :param k: number of nearest-neighbors to be returned
    :return: return list of k line indixes referring to the k nearest neighbors of x in X
    """
    distances = [np.linalg.norm(data_matrix[i]-data_vector) for i in range(len(data_matrix))]
    return np.argsort(distances)[:k]