import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from KNN_model import Model

style = {
        "text.color": "ffffff", # text color of title
        "axes.facecolor": "1a1a1a", # grid background
        "axes.edgecolor": "ffffff", # edge of graph
        "axes.labelcolor": "ffffff", # axes label
        # axis ticks
        "xtick.color": "ffffff",
        "ytick.color": "ffffff",
        "grid.color": "4c4c4c", # grid line
        # outer background color
        "figure.facecolor": "1a1a1a",
        "figure.edgecolor": "1a1a1a",
        "savefig.facecolor": "1a1a1a",
        "savefig.edgecolor": "1a1a1a"
        }

def plot_2D(x,y,name="Coin measurement"):
    plt.rcParams.update(style)
    plt.scatter(x, y)
    plt.title(name)
    plt.xlabel("Count")
    plt.ylabel("Value")
    plt.show()

def plot_4D(x,y,z,c):
    plt.rcParams.update(style)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.w_xaxis.set_pane_color((0,0,0,0))
    ax.w_yaxis.set_pane_color((0,0,0,0))
    ax.w_zaxis.set_pane_color((0,0,0,0))

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