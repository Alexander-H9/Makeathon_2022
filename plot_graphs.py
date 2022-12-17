"""Plotting graphs"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

style = {
        "text.color": "ffffff",
        "axes.facecolor": "333333",
        "axes.edgecolor": "ffffff",
        "axes.labelcolor": "ffffff",
        "xtick.color": "ffffff",
        "ytick.color": "ffffff",
        "grid.color": "4c4c4c",
        "figure.facecolor": "333333",
        "figure.edgecolor": "333333",
        "savefig.facecolor": "333333",
        "savefig.edgecolor": "333333"
        }

def plot_2d(x,y,name,path,filetype):
    """This function will plot 2D coordinates"""
    plt.rcParams.update(style)
    plt.scatter(x, y)
    plt.title(name)
    plt.xlabel("Count")
    plt.ylabel("Value")
    plt.savefig(path+"/"+name+"."+filetype,dpi='figure')
    plt.close()

def plot_4d(model,name,path,filetype):
    """This function will plot 4D graphs"""
    plt.rcParams.update(style)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.w_xaxis.set_pane_color((0,0,0,0))
    ax.w_yaxis.set_pane_color((0,0,0,0))
    ax.w_zaxis.set_pane_color((0,0,0,0))
    ax.view_init(elev=20., azim=225)
    x_list,y_list,z_list,c_list = ([] for _ in range(4))
    print(model)
    for coin in model:
        x_list.append(model[coin][0])
        y_list.append(model[coin][1])
        z_list.append(model[coin][2])
        c_list.append(model[coin][3])

    img = ax.scatter(x_list, y_list, z_list, c=c_list, cmap=plt.spring())
    fig.colorbar(img)
    plt.savefig(path+"/"+name+"."+filetype,dpi='figure')
    plt.close()

def plot_evaluation(accuracy_coins:dict):
    """
    Bar plot for the evaluation
    """
    values = accuracy_coins.values()
    labels = accuracy_coins.keys()
    y_pos = np.arange(len(labels))

    ax = plt.axes()

    plt.title("Evaluation")
    plt.bar(y_pos, values)
    plt.xticks(y_pos, labels)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.figure
    plt.subplots_adjust(bottom=0.15)
    plt.savefig("evaluation.jpg", dpi=600)
    plt.close()