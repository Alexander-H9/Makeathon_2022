import matplotlib.pyplot as plt
import numpy as np
from KNN_model import Model



def plot_2D(x,y):
    plt.scatter(x, y, color="black")
    plt.title("Coin measurement")
    plt.xlabel("Count")
    plt.ylabel("Value")
    plt.show()

def plot_4D(x,y,z,c):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    img = ax.scatter(x, y, z, c=c, cmap=plt.viridis())
    fig.colorbar(img)
    plt.show()

if __name__ == "__main__":
    model_large = Model("large.json","large")
    np_model_large = np.array(list(model_large.model.values()))
    x,y,z,c = ([] for _ in range(4))
    for coin in np_model_large:
        for entry in coin:
            x.append(entry[0])
            y.append(entry[1])
            z.append(entry[2])
            c.append(entry[3])
    plot_4D(x,y,z,c)