#!/usr/bin/env python
# coding: utf-8

import sqlite3

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
            exit(-1)

    def create_table(self):
        """
        This Method will create the Database Tables if they dont already exist
        """
        sql = """CREATE TABLE IF NOT EXISTS coins (
            id integer PRIMARY KEY,
            name text NOT NULL,
            minL integer NOT NULL,
            minR integer NOT NULL,
            maxM integer NOT NULL,
            length integer NOT NULL)"""
        self.cursor.execute(sql)

    def create_coin(self, coin):
        """
        Create a new coin
        :param coin:
        :return:
        """
        try:
            sql = """INSERT INTO coins(name,minL,minR,maxM,length) VALUES(?,?,?,?,?)"""
            self.cursor.execute(sql, coin)
            self.conn.commit()
        except Exception as exception:
            print("Error on creating coin: ", exception)

    def update_coin(self, coin):
        """
        update coin
        :param coin:
        :return:
        """
        try:
            sql = """UPDATE coins SET name = ?, minL = ?, minR = ?, maxM = ?, length = ? WHERE name = ?"""
            self.cursor.execute(sql, coin)
            self.conn.commit()
        except Exception as exception:
            print("Error on updating coin: ", exception)

    def select_all_coins(self):
        """
        Query all rows in the coins table
        :param conn: the Connection object
        :return:
        """
        try:
            sql = """SELECT * FROM coins"""
            data = self.cursor.execute(sql).fetchall()
            return (data)
        except Exception as exception:
            print("Error on selecting *: ", exception)
            return None

    def delete_coin(self, name):
        """
        Delete a coin by coin name
        :param conn:  Connection to the SQLite database
        :param name: name of the coin
        :return:
        """
        try:
            sql = """DELETE FROM coins WHERE name=?"""
            self.cursor.execute(sql, (name,))
            self.conn.commit()
        except Exception as exception:
            print("Error on deleting coin: ", exception)


if __name__ == "__main__":

    database = Dao("database.sqlite")

    coin_2euro = ('2 Euro', 202, 155, 645, 170)
    database.create_coin(coin_2euro)

    database.update_coin(("1 Euro", 203, 155, 645, 170, "2 Euro"))
    database.select_all_coins()

        # database.delete_coin("2 Euro")