"""This is main"""
#import threading
from flask import Flask, request, jsonify, render_template

from databaseaccess import Dao, combine_key
from plot_graphs import plot_2d,plot_4d
from KNN_model import Model

#from io_link import Inductor
#from stepper import Stepper, SEQ8

app = Flask(__name__)

## ----- GET ----- ##

@app.route("/")
def index():
    """Loading index page"""
    return render_template("index.html")

@app.route("/admin")
def admin():
    """Loading admin page"""
    return render_template("admin.html")

@app.route("/load/currencies")
def load_currencies():
    """Loading all trained currencies from database"""
    database = Dao("database.sqlite")
    return jsonify(database.get_currencies())

@app.route("/load/values")
def load_values():
    """Loading all trained values for given currency from database"""
    database = Dao("database.sqlite")

    currency = request.args.get('currency', type = str)
    return jsonify(database.get_coinvalues(currency))

@app.route("/load/stats")
def load_stats():
    """Loading amound of coins and currencies"""
    database = Dao("database.sqlite")
    return jsonify(database.get_stats())

@app.route("/scan")
def scan():
    """Scanning a coin"""
    print("Scanne Münze")
    model = Model("large", True)
    return model.predict(measurement())

## ----- POST ----- ##

@app.route("/coin/add", methods=["POST"])
def coin_add():
    """Scanning a new coin, add it to database and generate 2d plots of trainingdata"""
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
    """Training KNN model from all trainingdata in the database"""
    database = Dao("database.sqlite")
    try:
        model = Model("large", True)
        database.save_model(model.model)
        plot_4d(model.model,"4D Models","./static/images","png")
        return {}
    except Exception as exception:
        print(exception)
        return exception,400

## ----- DELETE ----- ##

@app.route("/delete", methods=["DELETE"])
def delete():
    """Deleting all entries of that coin from all database tables"""
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
    """Starting stepper motor and measurement"""
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
