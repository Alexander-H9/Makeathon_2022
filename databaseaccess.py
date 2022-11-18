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
            value integer NOT NULL,
            currency text NOT NULL,
            measurement blob NOT NULL)"""
        self.cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS models (
            id integer PRIMARY KEY AUTOINCREMENT,
            value integer NOT NULL,
            currency text NOT NULL,
            modelvalues blob NOT NULL)"""
        self.cursor.execute(sql)

    def save_training_data(self, value, currency, data):
        """
        This Method will save the trainingdata to the Database
        """
        try:
            sql = "INSERT INTO trainingdata VALUES (NULL,?,?,?)"
            self.cursor.execute(sql, (value,currency,json.dumps(data)))
            self.conn.commit()
            self.get_model_labels()
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
                key = str(value)+ " " + currency
                if key not in trainingdata:
                    trainingdata[key] = [json.loads(measurement)]
                else:
                    trainingdata[key].append(json.loads(measurement))
            return trainingdata
        except Exception as exception:
            print(exception)
            return None

    def get_model_labels(self):
        """
        This Method will return all labels"""
        try:
            sql = "SELECT value, currency FROM trainingdata"
            data = self.cursor.execute(sql).fetchall()
            labels = []
            for value,currency in data:
                label = str(value) + " " + currency
                if label not in labels:
                    labels.append(label)
            return labels
        except Exception as exception:
            print(exception)
            return None