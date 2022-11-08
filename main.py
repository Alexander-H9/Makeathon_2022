#!/usr/bin/env python
# coding: utf-8

import time
import threading
import matplotlib.pyplot as plt
import numpy as np

from io_link import Inductor, Socket
from stepper import Stepper, SEQ8
from KNN import prepData, X, getKNearestNeighbors

def plotData(x, y):
    plt.scatter(x, y, color="black")
    plt.title("Coin measurement")
    plt.xlabel("Count")
    plt.ylabel("Value")
    #plt.show()
    plt.savefig("/home/pi/IFM/Makeathon2022-main/plot.png")

if __name__ == "__main__":
    Sensor = Inductor()
    Motor = Stepper(SEQ8, 0.002)

    thread_motor = threading.Thread(target=Motor.run, args=(185, -1))
    thread_motor.start()

    data = []
    t_end = time.time() + 4
    while thread_motor.is_alive():
        val = Sensor.getValue()
        if val < 1000:
            data.append(val)
    
    plotData([y for y in range(len(data))], [x for x in data])

    x = prepData(data)
    k = 2
    idx_knn = getKNearestNeighbors(x, X, k)
    print("The k Nearest Neighbors of x =", x ,"are the following vectors:")
    for i in range(k):
        idx=idx_knn[i]
        print("The", i+1, "th nearest neighbor is: X[",idx,"] =",X[idx],"with distance", np.linalg.norm(X[idx]-x))
    
    PwrSocket = Socket()
    if idx_knn[0] == 0:
        PwrSocket.setPort(True)

    
    
