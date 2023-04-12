import sqlite3
from lab1.  confings.config import SQLITE as connection

# class to work with sqlite db
class SQLITE:
    def __init__(self):
        self.database = connection.get("filename")
        self.table_values = {1: ["address", "varchar(100)"],
                             2: ["buildingtype", "varchar(45)"],
                             3: ["apartmenttype", "varchar(45)"],
                             4: ["square", "float"],
                             5: ["rooms", "int"],
                             6: ["balcony", "boolean"],
                             7: ["floor", "int"],
                             8: ["price", "float"]}

    # create table with custom fields
    def create(self, values):
        try:
            con = sqlite3.connect(self.database)
            cursor = con.cursor()
            params = []
            for i in values:
                params.append(self.table_values.get(i)[0])
                params.append(self.table_values.get(i)[1])
            print(params)
            cursor.execute(f'CREATE TABLE apartments ({params[0]} {params[1]}, {params[2]} {params[3]}, {params[4]} {params[5]} '
                  f')')
        except Exception as ex:
            print(ex)

    # delete table
    def delete(self):
        try:
            con = sqlite3.connect(self.database)
            cursor = con.cursor()
            cursor.execute("drop table apartments")
            con.commit()
            con.close()
        except Exception as ex:
            print(ex)

    # insert data in table
    def insert_data(self, values):
        try:
            con = sqlite3.connect(self.database)
            cursor = con.cursor()
            for value in values:
                cursor.execute("INSERT INTO apartments VALUES (?, ?, ?)", value)
                con.commit()
        except Exception as ex:
            print(ex)

    # get data from table
    def get_data(self):
        try:
            con = sqlite3.connect(self.database)
            cursor = con.cursor()
            try:
                cursor.execute("SELECT * FROM apartments")
                rows = cursor.fetchall()
                return rows
            finally:
                con.close()
        except Exception as ex:
            print(ex)