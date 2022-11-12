from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from trainKNN import Model

"""
creating 4D data plots for presentation
"""

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

model_large = Model("large.json","large")
np_model_large = np.array(list(model_large.model.values()))

x,y,z,c = ([] for _ in range(4))
for coin in np_model_large:
    for entry in coin:
        x.append(entry[0])
        y.append(entry[1])
        z.append(entry[2])
        c.append(entry[3])

img = ax.scatter(x, y, z, c=c, cmap=plt.viridis())
fig.colorbar(img)
plt.show()
