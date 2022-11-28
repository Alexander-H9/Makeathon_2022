"""This Module manages the access to the SQLITE Database"""
import sqlite3
import sys
import json

class Dao:
    """
    This Class provides all the needed Methods to interact with the SQLite Database
    """
    def __init__(self, dbfile):
        try:
            self.conn = sqlite3.connect(dbfile, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_table()
        except Exception as exception:
            print(exception)
            sys.exit(-1)

    def create_table(self):
        """
        Create the Database Tables if they dont already exist
        """
        sql = """CREATE TABLE IF NOT EXISTS trainingdata (
            id integer PRIMARY KEY AUTOINCREMENT,
            value float NOT NULL,
            currency text NOT NULL,
            measurement blob NOT NULL)"""
        self.cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS models (
            id integer PRIMARY KEY AUTOINCREMENT,
            value float NOT NULL,
            currency text NOT NULL,
            modeldata blob NOT NULL)"""
        self.cursor.execute(sql)

# --------------- TRAININGDATA TABLE --------------- #

    def save_training_data(self, value, currency, data):
        """
        This Method will save the trainingdata to the Database
        """
        try:
            sql = "INSERT INTO trainingdata VALUES (NULL,?,?,?)"
            self.cursor.execute(sql, (value,currency,json.dumps(data)))
            self.conn.commit()
        except Exception as exception:
            print(exception)

    def load_all_training_data(self):
        """
        This Method will return all trainingdata as a dictionary"""
        try:
            sql = "SELECT * FROM trainingdata"
            data = self.cursor.execute(sql).fetchall()
            trainingdata = dict()
            for _, value, currency, measurement in data:
                key = combine_key(value,currency)
                if key not in trainingdata:
                    trainingdata[key] = [json.loads(measurement)]
                else:
                    trainingdata[key].append(json.loads(measurement))
            return trainingdata
        except Exception as exception:
            print(exception)
            return None

    def delete_coin_trainingdata(self,value, currency):
        """
        This Method will delete all trainingdata for the given coin
        """
        try:
            sql = "DELETE FROM trainingdata WHERE value=? AND currency=?"
            self.cursor.execute(sql, (value,currency))
            self.conn.commit()
        except Exception as exception:
            print(exception)

# --------------- MODELS TABLE --------------- #

    def save_model(self, data):
        """
        This Method will delete all trained models and save the new trained model to the Database
        """
        try:
            # CLEAR DATABASE
            self.cursor.execute("DELETE FROM models")

            for key in data:
                value,currency = split_key(key)

                sql = "INSERT INTO models VALUES (NULL,?,?,?)"
                self.cursor.execute(sql, (value,currency,json.dumps(data[key])))
            self.conn.commit()
        except Exception as exception:
            print(exception)

    def load_all_models(self):
        """
        This Method will return all trained models as a dictionary"""
        try:
            sql = "SELECT * FROM models"
            data = self.cursor.execute(sql).fetchall()
            models = dict()
            for _, value, currency, model in data:
                key = combine_key(value,currency)
                models[key] = json.loads(model)
            return models
        except Exception as exception:
            print(exception)
            return None

    def get_model_labels(self):
        """
        This Method will return all labels"""
        try:
            sql = "SELECT value, currency FROM models"
            data = self.cursor.execute(sql).fetchall()
            labels = []
            for value,currency in data:
                label = combine_key(value,currency)
                labels.append(label)
            return labels
        except Exception as exception:
            print(exception)
            return None

    def get_currencies(self):
        """
        This Method returns all currencies"""
        try:
            sql = "SELECT currency FROM models"
            data = self.cursor.execute(sql).fetchall()
            return list(dict.fromkeys([c[0] for c in data]))
        except Exception as exception:
            print(exception)
            return None

    def get_coinvalues(self,currency):
        """
        This Method returns all values for the given currency"""
        try:
            sql = "SELECT value FROM models WHERE currency=?"
            data = self.cursor.execute(sql,(currency,)).fetchall()
            return sorted([v[0] for v in data],reverse=True)
        except Exception as exception:
            print(exception)
            return None

    def get_stats(self):
        """
        This Method returns amount of coins and currencies"""
        try:
            sql = "SELECT value, currency FROM models"
            data = self.cursor.execute(sql).fetchall()
            valuecount = 0
            currencies = []
            for _,currency in data:
                valuecount+=1
                currencies.append(currency)
            return valuecount, len(set(currencies))
        except Exception as exception:
            print(exception)
            return None

    def delete_coin_model(self,value, currency):
        """
        This Method will delete the trained model for the given coin
        """
        try:
            sql = "DELETE FROM models WHERE value=? AND currency=?"
            self.cursor.execute(sql, (value,currency))
            self.conn.commit()
        except Exception as exception:
            print(exception)

def combine_key(value,currency):
    """Combine value and currency"""
    value = str(value)
    if value.endswith(".0"):
        value=value[:-2]
    return value + " " + currency

def split_key(key):
    """split value and currency"""
    return key.split(" ")
