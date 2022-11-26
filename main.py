import threading
from flask import Flask, request, jsonify, render_template
from databaseaccess import Dao
import matplotlib.pyplot as plt
import numpy as np

from io_link import Inductor
from stepper import Stepper, SEQ8
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
        return {}
    except Exception as exception:
        print(exception)
        return exception,400

@app.route("/train", methods=["POST"])
def train():
    database = Dao("database.sqlite")
    try:

        #   ----- DUMMYCODE -----   #
        print("ICH TRAINIERE DAS MODEL")
        trainingdata = database.load_all_training_data()
        model = dict()
        for key in trainingdata:
            model[key] = trainingdata[key][0]
        database.save_model(model)
        #   ----- DUMMYCODE ENDE -----   #


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


# IMPLEMENTIER MICH ANDI :)
def measurement():
    """
    Starts stepper Motor and measurement.
    Returns Array of all measurements.
    """
    Sensor = Inductor()
    Motor = Stepper(SEQ8, 0.002)

    thread_motor = threading.Thread(target=Motor.run, args=(180, -1))
    thread_motor.start()

    data = []
    while thread_motor.is_alive():
        val = Sensor.getValue()
        if val < 1000:
            data.append(val)

    return data   # Ungekürzte Messdaten

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
