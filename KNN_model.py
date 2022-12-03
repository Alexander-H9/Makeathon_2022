import json
import numpy as np
from databaseaccess import Dao
# from main import measurement as mes

class Model:
    """
    Class representing a Model
    """
    def __init__(self, model_type, model_from_db=False, name="default"):
        self.name: str = name
        self.model_type: str = model_type
        self.database = Dao("database.sqlite")
        self.key_mapping = {0: "2€", 1: "1€", 2: "0.5€", 3: "0.20€",
                            4: "0.10", 5: "0.05€", 6: "0.02€", 7: "0.01€"}

        if model_from_db:
            self.model = self.database.load_all_training_data()
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


    def predict(self, measurement):
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

        if len(self.database.get_model_labels()) < idx_knn[0]:
            print("ERROR Max, da läuft irgend was nicht ganz rund in der Datenbank")
            exit()

        return self.database.get_model_labels()[idx_knn[0]]


    def evaluate(self, y):
        """
        evaluate the model and returns the accuracy
        """

        ITERATIONS = 10
        true_prediction = 0

        for _ in range(ITERATIONS):

            measurement = [12,23,34,45,56,67,678] # mes()
            if len(measurement) != 4:
                measurement = prep_data(measurement)

            if self.predict(measurement) == y:
                true_prediction += 1

        accuracy = round(true_prediction/ITERATIONS, 2)*100
        return accuracy


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



if __name__ == "__main__":

    messwerte = [210, 838, 985, 340, 864, 130, 719, 255, 782, 992,
                732, 497, 811, 623, 172, 700, 283, 951, 504, 770,
                516, 51, 900, 806, 197, 485, 1000, 987, 573, 6,
                758, 653, 386, 423, 398, 649, 34, 184, 519, 901,
                952, 447, 319, 199, 714, 302, 235, 161, 767, 958]

    # old working models
    # model_small = Model("model_type="small", name="model_1.json")
    # model_large = Model("model_2.json", name=model_type="large")

    # test models
    # model_small = Model(model_type="small", name="model_small.json")
    # model_large = Model(model_type="large", name="model_large.json")

    # current models
    model_small = Model(model_type="small", name="small.json")
    model_large = Model(model_type="large", name="large.json")

    model_large.create_small_model_from_training_data()
    print(model_large.predict(messwerte))
    print(model_large.evaluate("0.1 Euro"))
    exit()

    # model_small.update_small_model("200", (202, 155, 645, 170))
    # model_large.update_large_model("200", (202, 155, 645, 170))

    x = prep_data(messwerte)

    np_model_small = np.array(list(model_small.model.values()))
    np_model_large = np.array(list(model_large.model.values()))

    # remove the amount column which is only required to train the small model
    if model_small.model_type == "small":
        np_model_small = np.delete(np_model_small, 4, 1)

    # remove the amount column which is only required to train the small model
    if model_large.model_type == "small":
        np_model_large = np.delete(np_model_large, 4, 1)

    idx_knn_small = get_k_nearest_neighbors(x, np_model_small, 1)
    idx_knn_large = get_k_nearest_neighbors(x, np_model_large, 1)

    print(f'Small model index: {idx_knn_small}')
    print(f'Large model index: {idx_knn_large} \n')

    print(f'Small model prediction: {model_small.key_mapping[idx_knn_small[0]]}')
    print(f'Large model prediction: {model_large.key_mapping[idx_knn_large[0]]}')
