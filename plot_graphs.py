import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
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
        "figure.facecolor": "333333",
        "figure.edgecolor": "333333",
        "savefig.facecolor": "333333",
        "savefig.edgecolor": "333333"
        }

def plot_2d(x,y,name,path,type):
    """This function will plot 2D coordinates"""
    plt.rcParams.update(style)
    plt.scatter(x, y)
    plt.title(name)
    plt.xlabel("Count")
    plt.ylabel("Value")
    plt.savefig(path+"/"+name+"."+type,dpi='figure')

def plot_4d(x,y,z,c,name,path,type):
    """This function will plot 4D graphs"""
    plt.rcParams.update(style)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.w_xaxis.set_pane_color((0,0,0,0))
    ax.w_yaxis.set_pane_color((0,0,0,0))
    ax.w_zaxis.set_pane_color((0,0,0,0))

    img = ax.scatter(x, y, z, c=c, cmap=plt.viridis())
    fig.colorbar(img)
    plt.savefig(path+"/"+name+"."+type,dpi='figure')

if __name__ == "__main__":
    model = {'1 Euro': [270, 219, 458, 141, 6], '0.5 Euro': [716, 664, 746, 131, 1], '2 Euro': [287, 198, 726, 165, 4]}
    x,y,z,c = ([] for _ in range(4))
    for coin in model:
        print(model[coin])
        x.append(model[coin][0])
        y.append(model[coin][1])
        z.append(model[coin][2])
        c.append(model[coin][3])
    plot_4d(x,y,z,c,"test","./static/images","png")
