import json
import numpy as np
from KNN import prepData, getKNearestNeighbors, X

class Model:
    

    def __init__(self, name, model_type):
        self.name: str = name
        self.model_type: str = model_type
        self.keyMapping = {0: "2€", 1: "1€", 2: "0.5€", 3: "0.20€", 4: "0.10", 5: "0.05€", 6: "0.02€", 7: "0.01€"}

        try:
            with open(f'models/{self.name}', 'r') as j:
                self.model: dict = json.loads(j.read())

        except FileNotFoundError:
            print("Creating a new model ", self.name)
            with open(f'models/{self.name}', 'w') as j:
                pass

            self.model: dict = {"200": [], "100": [], "50": [], "20": [], "10": [], "5": [], "2": [], "1": []}
            self.write_model()


    def write_model(self):
        """Write the model to a json file"""

        with open(f'models/{self.name}', 'w') as j:
            j.write(json.dumps(self.model, indent=4))


    def update_small_model(self, coin: str, wight_update):
        """Update one coin wight for the small model"""

        # if the model has no enty 
        if len(self.model[coin]) == 0:
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
        """Update one coin wight for the large model"""
        if len(self.model[coin]) == 0:
            print(f"Add new entry for {coin} coins at model {self.name}")

        self.model[coin].append(list(wight_update))
        self.write_model()
        

# model_small = Model("model_1.json", model_type="small")
# model_large = Model("model_2.json", model_type="large")

model_small = Model("model_small.json", model_type="small")
model_large = Model("model_large.json", model_type="large")

model_small.update_small_model("50", (202, 155, 645, 170))
model_large.update_large_model("100", (202, 155, 645, 170))



# messwerte = [210, 838, 985, 340, 864, 130, 719, 255, 782, 992, 732, 497, 811, 623, 172, 700, 283, 951, 504, 770, 516, 51, 900, 806, 197, 485, 1000, 987, 573, 6, 758, 653, 386, 423, 398, 649, 34, 184, 519, 901, 952, 447, 319, 199, 714, 302, 235, 161, 767, 958]

# x = prepData(messwerte)

# np_model_small = np.array(list(model_small.model.values()))
# np_model_large = np.array(list(model_large.model.values()))

# if model_small.model_type == "small": np_model_small = np.delete(np_model_small, 4, 1) # remove the amount column which is only required to train the small model
# if model_large.model_type == "small": np_model_large = np.delete(np_model_large, 4, 1) # remove the amount column which is only required to train the small model

# idx_knn_small = getKNearestNeighbors(x, np_model_small, 1)
# idx_knn_large = getKNearestNeighbors(x, np_model_large, 1)

# print(f'Small model index: {idx_knn_small}')
# print(f'Large model index: {idx_knn_large} \n')

# print(f'Small model prediction: {model_small.keyMapping[idx_knn_small[0]]}')
# print(f'Large model prediction: {model_large.keyMapping[idx_knn_large[0]]}')