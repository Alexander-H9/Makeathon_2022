import json


class Model:
    

    def __init__(self, name):
        self.name: str = name

        with open(f'models/{self.name}', 'r') as j:

            self.model = json.loads(j.read())


    def update_minimal_model(self, coin: str, wight_update):
        """Update one coin wight for the small model where the neighbours k is always k = 1"""

        wights = self.model[coin][:-1]
        amount = self.model[coin][4]

        for idx,wight in enumerate(wights):

            wights[idx] = int(round((wight_update[idx]/amount + wight*((amount-1)/amount)), 0))

        amount += 1
        wights.append(amount)
        self.model[coin] = wights

        with open(f'models/{self.name}', 'w') as j:
            j.write(json.dumps(self.model, indent=4))


    def update_large_model(self, coin: str, wight_update):
        """Update one coin wight for the large model where the neighbours k is can be k <= 1"""
        pass


c = Model("model_1.json")

c.update_minimal_model("200", (202, 155, 645, 170))