import csv
import sqlite3
from sqlite3 import Error


def create_connection():
    try:
        return sqlite3.connect(':memory:')
    except Error as e:
        print(e)


def insert_product(db, products):
    sql = ''' INSERT INTO products(buyDate, value, device, client)
                 VALUES(?,?,?,?)'''
    cur = db.cursor()
    cur.execute(sql, products)
    db.commit()


def select_db(db, sqlite_select_query):
    cur = db.cursor()
    cur.execute(sqlite_select_query)
    return cur.fetchall()


def create_temp_table(db):
    sql_ddl = """ CREATE TABLE IF NOT EXISTS products (
                                            id integer PRIMARY KEY,
                                            buyDate TEXT,
                                            value INTEGER,
                                            device string,
                                            client INTEGER
                                        ); """
    try:
        c = db.cursor()
        c.execute(sql_ddl)
    except Error as e:
        print(e)


def getLessDate():
    return """SELECT * from products order by buydate asc limit 1"""


def getBiggerDate():
    return """SELECT * from products order by buydate desc limit 1"""


def getTotalShipping():
    return """SELECT sum(value) from products"""


def getDistinctDevices():
    return """SELECT distinct device from products"""


def getPriceByShipping():
    return """SELECT device,sum(value) from products group by device"""


if __name__ == '__main__':

    # creating a database connection (local database sqlite)
    db = create_connection()

    # create a table if exist, if not create it
    create_temp_table(db)

    # insert csv values in database, line by line
    with open("source.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            insert_product(db, row)

    lessDate = select_db(db, getLessDate())[0][1]
    biggerDate = select_db(db, getBiggerDate())[0][1]
    getTotalShipping = select_db(db, getTotalShipping())[0][0]
    getPriceByShipping = select_db(db, getPriceByShipping())

    result = """
    Menor Data: {lessDate}
    Maior Data: {biggerDate}
    Total Frete: R$ {getTotalShipping}
    Quantidade de Envios: 6
    Quantidade de Equipamentos Distintos: 3
    Frete Por Equipamento:
    """.format(lessDate=lessDate,
               biggerDate=biggerDate,
               getTotalShipping=getTotalShipping)
    print(result)
    for item in getPriceByShipping:
        print("     - ", item[0], "R$ ", item[1])


        
