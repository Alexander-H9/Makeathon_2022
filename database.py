#!/usr/bin/env python
# coding: utf-8

import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def create_coin(conn, coin):
    """
    Create a new coin
    :param conn:
    :param coin:
    :return:
    """

    sql = ''' INSERT INTO coins(name,minL,minR,maxM,length)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, coin)
    conn.commit()
    return cur.lastrowid

def update_coin(conn, coin):
    """
    update coin
    :param conn:
    :param coin:
    :return:
    """
    sql = ''' UPDATE coins
              SET name = ? ,
                  minL = ? ,
                  minR = ? ,
                  maxM = ? ,
                  length = ?
              WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, coin)
    conn.commit()

def select_all_coins(conn):
    """
    Query all rows in the coins table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM coins")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def delete_coin(conn, name):
    """
    Delete a coin by coin name
    :param conn:  Connection to the SQLite database
    :param name: name of the coin
    :return:
    """
    sql = 'DELETE FROM coins WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (name,))
    conn.commit()


if __name__ == "__main__":
    # create a database connection
    conn = create_connection("/home/pi/IFM/Makeathon2022-main/database.db")

    # sql_create_coins_table = """ CREATE TABLE IF NOT EXISTS coins (
    #                                     id integer PRIMARY KEY,
    #                                     name text NOT NULL,
    #                                     minL integer NOT NULL,
    #                                     minR integer NOT NULL,
    #                                     maxM integer NOT NULL,
    #                                     length integer NOT NULL
    #                                 ); """

    if conn is not None:
        # create projects table
        # create_table(conn, sql_create_coins_table)

        coin_2euro = ('2 Euro', 202, 155, 645, 170)
        create_coin(conn, coin_2euro)

        # update_coin(conn, ("2 Euro", 203, 155, 645, 170, "1 Euro"))

        select_all_coins(conn)

        # delete_coin(conn, "2 Euro")

    else:
        print("Error! cannot create the database connection.")