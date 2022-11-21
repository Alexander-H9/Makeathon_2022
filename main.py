import threading
from flask import Flask, request, jsonify, render_template
from databaseaccess import Dao
import matplotlib.pyplot as plt
import numpy as np

from io_link import Inductor
#from stepper import Stepper, SEQ8
from KNN import prep_data, get_k_nearest_neighbors
from KNN_model import Model

app = Flask(__name__)

## ----- GET ----- ##

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/coins/load")
def coin_load():
    data = {
            "values": ["2,00", "1,00", "0,50", "0,20", "0,10", "0,05", "0,02", "0,01"],
            "currencies": ["Euro","Kronen","Dollar","Pounds","Alexcoin"]
    }
    return jsonify(data)

## ----- POST ----- ##

@app.route("/coin/add", methods=["POST"])
def coin_add():
    database = Dao("database.sqlite")

    value = request.args.get('value', type = int)
    currency = request.args.get('currency', type = str)
    try:
        data = measurement()
        database.save_training_data(value,currency,data)
        return {}
    except Exception as exception:
        print(exception)
        return exception,400

@app.route("/train", methods=["POST"])
def train():
    try:
        print("ICH TRAINIERE DAS MODEL")
        return {}
    except Exception as exception:
        print(exception)
        return exception,400




# BENUTZ MICH ALEX :)
"""
database = Dao()
dictionary = database.load_all_training_data()
"""

# IMPLEMENTIER MICH ANDI :)
def measurement():
    """
    Starts stepper Motor and measurement.
    Returns Array of all measurements.
    """
    return [666,111,111,111,65]

if __name__ == "__main__":
    """Sensor = Inductor()
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

    plot_data_curve(list(range(len(data))), data)

    x = prep_data(data)
    print(x)

    # kNN_small.update_small_model("10", x)
    # kNN_large.update_large_model("10", x)

    np_model_small = np.array(list(model_small.model.values()))
    np_model_large = np.array(list(model_large.model.values()))

    print(np_model_small, np_model_large)

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

    print(f'Small model prediction: {model_small.keyMapping[idx_knn_small[0]]}')
    print(f'Large model prediction: {model_large.keyMapping[idx_knn_large[0]]}')
"""
    # PwrSocket = Socket()
    # if idx_knn[0] == 0:
    #     PwrSocket.setPort(True)

    app.run(debug=True, host="0.0.0.0")
