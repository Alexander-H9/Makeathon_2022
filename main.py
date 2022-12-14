"""This is main"""
import threading
from flask import Flask, request, jsonify, render_template
from measurement import measurement
from waitress import serve

from databaseaccess import Dao, combine_key, split_key
from plot_graphs import plot_2d,plot_4d, plot_evaluation
from KNN_model import Model

if not __debug__:
    from io_link import Inductor
    from stepper import Stepper

BANKACCOUNT = dict()

app = Flask(__name__)
database = Dao("database.sqlite")

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
    return jsonify(database.get_currencies())

@app.route("/load/values")
def load_values():
    """Loading all trained values for given currency from database"""
    currency = request.args.get('currency', type = str)
    return jsonify(database.get_coinvalues(currency))

@app.route("/load/stats")
def load_stats():
    """Loading amount of coins and currencies"""
    return jsonify(database.get_stats())

@app.route("/load/bankaccount")
def load_bankaccount():
    """Loading bankaccount values and currencies"""
    global BANKACCOUNT
    return jsonify(BANKACCOUNT)

@app.route("/scan")
def scan():
    """Scanning a coin"""
    model = Model(model_type="large", model_from_db=database.load_all_training_data())
    result = model.predict(measurement(), database.get_model_labels())
    value, currency = split_key(result)

    global BANKACCOUNT
    if currency in BANKACCOUNT:
        BANKACCOUNT[currency] += float(value)
    else:
        BANKACCOUNT[currency] = float(value)
    return result

@app.route("/evaluate")
def eval():
    model = Model(model_type="large", model_from_db=database.load_all_training_data())
    accuracy = model.evaluate(database.get_model_labels())
    plot_evaluation(accuracy)
    return {} 

## ----- POST ----- ##

@app.route("/coin/add", methods=["POST"])
def coin_add():
    """Scanning a new coin, add it to database and generate 2d plots of trainingdata"""
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
    try:
        model = Model(model_type="large", model_from_db=database.load_all_training_data())
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
    value = request.args.get('value', type = float)
    currency = request.args.get('currency', type = str)
    try:
        database.delete_coin_model(value,currency)
        database.delete_coin_trainingdata(value,currency)
        return {} 
    except Exception as exception:
        print(exception)
        return exception,400

if __name__ == "__main__":
    if __debug__:
        app.run(debug=True, host="0.0.0.0")
    else:
        serve(app, host="0.0.0.0", port=80)
