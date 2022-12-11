"""This Module manages the access to the SQLITE Database"""
import sqlite3
import traceback
import json

class Dao:
    """
    This Class provides all the needed Methods to interact with the SQLite Database
    """
    def __init__(self, dbfile):
        try:
            sqlite3.threadsafety = 1
            self.dbfile = dbfile
            self.create_tables()

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())

    def get_db_connection(self):
        """
        This Method opens a db connection
        """
        try:
            conn = sqlite3.connect(self.dbfile, check_same_thread=False)
            cursor = conn.cursor()
            return conn, cursor

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())

    def create_tables(self):
        """
        Create the Database Tables if they dont already exist
        """
        try:
            conn, cursor = self.get_db_connection()
            sql = """CREATE TABLE IF NOT EXISTS trainingdata (
                id integer PRIMARY KEY AUTOINCREMENT,
                value float NOT NULL,
                currency text NOT NULL,
                measurement blob NOT NULL)"""
            cursor.execute(sql)

            sql = """CREATE TABLE IF NOT EXISTS models (
                id integer PRIMARY KEY AUTOINCREMENT,
                value float NOT NULL,
                currency text NOT NULL,
                modeldata blob NOT NULL)"""
            cursor.execute(sql)
            conn.close()

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())

# --------------- TRAININGDATA TABLE --------------- #

    def save_training_data(self, value, currency, data):
        """
        This Method will save the trainingdata to the Database
        """
        try:
            conn, cursor = self.get_db_connection()
            sql = "INSERT INTO trainingdata VALUES (NULL,?,?,?)"
            cursor.execute(sql, (value,currency,json.dumps(data)))
            conn.commit()#
            conn.close()

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())

    def load_all_training_data(self):
        """
        This Method will return all trainingdata as a dictionary"""
        try:
            conn, cursor = self.get_db_connection()
            sql = "SELECT * FROM trainingdata"
            data = cursor.execute(sql).fetchall()
            conn.close()

            trainingdata = dict()
            for _, value, currency, measurement in data:
                key = combine_key(value,currency)
                if key not in trainingdata:
                    trainingdata[key] = [json.loads(measurement)]
                else:
                    trainingdata[key].append(json.loads(measurement))
            return trainingdata

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())
            return None

    def delete_coin_trainingdata(self,value, currency):
        """
        This Method will delete all trainingdata for the given coin
        """
        try:
            conn, cursor = self.get_db_connection()
            sql = "DELETE FROM trainingdata WHERE value=? AND currency=?"
            cursor.execute(sql, (value,currency))
            conn.commit()
            conn.close()

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())

# --------------- MODELS TABLE --------------- #

    def save_model(self, data):
        """
        This Method will delete all trained models and save the new trained model to the Database
        """
        try:
            conn, cursor = self.get_db_connection()
            cursor.execute("DELETE FROM models")    # CLEAR DATABASE

            for key in data:
                value,currency = split_key(key)

                sql = "INSERT INTO models VALUES (NULL,?,?,?)"
                cursor.execute(sql, (value,currency,json.dumps(data[key])))
            conn.commit()
            conn.close()

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())

    def load_all_models(self):
        """
        This Method will return all trained models as a dictionary"""
        try:
            conn, cursor = self.get_db_connection()
            sql = "SELECT * FROM models"
            data = cursor.execute(sql).fetchall()
            conn.close()

            models = dict()
            for _, value, currency, model in data:
                key = combine_key(value,currency)
                models[key] = json.loads(model)
            return models

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())
            return None

    def get_model_labels(self):
        """
        This Method will return all labels"""
        try:
            conn, cursor = self.get_db_connection()
            sql = "SELECT value, currency FROM models"
            data = cursor.execute(sql).fetchall()
            conn.close()

            labels = []
            for value,currency in data:
                label = combine_key(value,currency)
                labels.append(label)
            return labels

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())
            return None

    def get_currencies(self):
        """
        This Method returns all currencies"""
        try:
            conn, cursor = self.get_db_connection()
            sql = "SELECT currency FROM models"
            data = cursor.execute(sql).fetchall()
            conn.close()
            return list(dict.fromkeys([c[0] for c in data]))

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())
            return None

    def get_coinvalues(self,currency):
        """
        This Method returns all values for the given currency"""
        try:
            conn, cursor = self.get_db_connection()
            sql = "SELECT value FROM models WHERE currency=?"
            data = cursor.execute(sql,(currency,)).fetchall()
            conn.close()
            return sorted([v[0] for v in data],reverse=True)

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())
            return None

    def get_stats(self):
        """
        This Method returns amount of coins and currencies"""
        try:
            conn, cursor = self.get_db_connection()
            sql = "SELECT value, currency FROM models"
            data = cursor.execute(sql).fetchall()
            conn.close()

            valuecount = 0
            currencies = []
            for _,currency in data:
                valuecount+=1
                currencies.append(currency)
            return valuecount, len(set(currencies))

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())
            return None

    def delete_coin_model(self,value, currency):
        """
        This Method will delete the trained model for the given coin
        """
        try:
            conn, cursor = self.get_db_connection()
            sql = "DELETE FROM models WHERE value=? AND currency=?"
            cursor.execute(sql, (value,currency))
            conn.commit()
            conn.close()

        except sqlite3.Error as err:
            error_handler(err,traceback.format_exc())

def combine_key(value,currency):
    """Combine value and currency"""
    value = str(value)
    if value.endswith(".0"):
        value=value[:-2]
    return value + " " + currency

def split_key(key):
    """split value and currency"""
    return key.split(" ")

def error_handler(err,trace):
    """
    Print Errors that can occurr in the DB Methods
    """
    print(f"SQLite error: {err.args}")
    print("Exception class is: ", err.__class__)
    print("SQLite traceback: ")
    print(trace)
