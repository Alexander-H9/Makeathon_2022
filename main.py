"""This is main"""
import threading
from flask import Flask, request, jsonify, render_template
from databaseaccess import Dao, combine_key, split_key
import matplotlib.pyplot as plt
import numpy as np

from io_link import Inductor
#from stepper import Stepper, SEQ8
from KNN import prep_data, get_k_nearest_neighbors
from KNN_model import Model
from plot_graphs import plot_2d

app = Flask(__name__)

## ----- GET ----- ##

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/coins/load/currencies")
def coins_load_currencies():
    database = Dao("database.sqlite")
    return jsonify(database.get_currencies())

@app.route("/coins/load/values")
def coins_load_values():
    database = Dao("database.sqlite")

    currency = request.args.get('currency', type = str)
    return jsonify(database.get_coinvalues(currency))

## ----- POST ----- ##

@app.route("/coin/add", methods=["POST"])
def coin_add():
    database = Dao("database.sqlite")

    value = request.args.get('value', type = float)
    currency = request.args.get('currency', type = str)
    try:
        data = measurement()
        database.save_training_data(value,currency,data)
        plot_2d(list(range(len(data))),data,combine_key(value, currency),"./static/images","png")
        return {}
    except Exception as exception:
        print(exception)
        return exception,400

@app.route("/train", methods=["POST"])
def train():
    database = Dao("database.sqlite")
    try:

        model = Model("large", True)
        database.save_model(model.model)

        return {}
    except Exception as exception:
        print(exception)
        return exception,400

## ----- DELETE ----- ##

@app.route("/delete", methods=["DELETE"])
def delete():
    database = Dao("database.sqlite")

    value = request.args.get('value', type = float)
    currency = request.args.get('currency', type = str)
    try:
        database.delete_coin_model(value,currency)
        database.delete_coin_trainingdata(value,currency)
        return {}
    except Exception as exception:
        print(exception)
        return exception,400

def measurement():
    """
    Starts stepper Motor and measurement.
    Returns Array of all measurements.
    """
#    Sensor = Inductor()
#    Motor = Stepper(SEQ8, 0.002)

#    thread_motor = threading.Thread(target=Motor.run, args=(180, -1))
#    thread_motor.start()

    data = []
#    while thread_motor.is_alive():
#        val = Sensor.get_value()
#        if val < 1000:
#            data.append(val)

    return data   # Ungekürzte Messdaten

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
