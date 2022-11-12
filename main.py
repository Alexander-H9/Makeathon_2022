#!/usr/bin/env python
# coding: utf-8

import time
import threading
import matplotlib.pyplot as plt
import numpy as np

from io_link import Inductor, Socket
from stepper import Stepper, SEQ8
from KNN import prepData, X, getKNearestNeighbors
from trainKNN import Model

def plotDataCurve(x, y):
    plt.scatter(x, y, color="black")
    plt.title("Coin measurement")
    plt.xlabel("Count")
    plt.ylabel("Value")
    #plt.show()
    plt.savefig("/home/pi/IFM/Makeathon2022-main/plot.png")

if __name__ == "__main__":
    Sensor = Inductor()
    Motor = Stepper(SEQ8, 0.002)

    model_small = Model("small.json","small")
    model_large = Model("large.json","large")

    thread_motor = threading.Thread(target=Motor.run, args=(180, -1))
    thread_motor.start()

    data = []
    while thread_motor.is_alive():
        val = Sensor.getValue()
        if val < 1000:
            data.append(val)
    
    plotDataCurve([y for y in range(len(data))], [x for x in data])

    x = prepData(data)
    print(x)

    # kNN_small.update_small_model("10", x)
    # kNN_large.update_large_model("10", x)
    
    np_model_small = np.array(list(model_small.model.values()))
    np_model_large = np.array(list(model_large.model.values()))

    print(np_model_small, np_model_large)
    if model_small.model_type == "small": np_model_small = np.delete(np_model_small, 4, 1) # remove the amount column which is only required to train the small model
    if model_large.model_type == "small": np_model_large = np.delete(np_model_large, 4, 1) # remove the amount column which is only required to train the small model

    idx_knn_small = getKNearestNeighbors(x, np_model_small, 1)
    idx_knn_large = getKNearestNeighbors(x, np_model_large, 1)

    print(f'Small model index: {idx_knn_small}')
    print(f'Large model index: {idx_knn_large} \n')

    print(f'Small model prediction: {model_small.keyMapping[idx_knn_small[0]]}')
    print(f'Large model prediction: {model_large.keyMapping[idx_knn_large[0]]}')
    
    # PwrSocket = Socket()
    # if idx_knn[0] == 0:
    #     PwrSocket.setPort(True)
