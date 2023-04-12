import re
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QHeaderView, QMessageBox

from lab1.Databases.POSTGRESQL import POSTGRESQL
from lab1.Databases.MYSQL import MYSQL
from lab1.Databases.SQLITE import SQLITE


# main window class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("Main.ui", self)

        # add objects to work with DBC
        self.postgres = POSTGRESQL()
        self.msql = MYSQL()
        self.sqlite = SQLITE()

        # connect button objects with methods
        self.SELECT.clicked.connect(self.select_table_data)
        self.UPDATE.clicked.connect(self.update_table_data)
        self.ADD.clicked.connect(self.add_table_data)
        self.DELETE.clicked.connect(self.delete_table_data)
        self.IMPORT.clicked.connect(self.import_data)

        # resize table headers
        header = self.MSQLTABLE.horizontalHeader()
        for i in range(0, 9):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        header = self.POSTGRESTABLE.horizontalHeader()
        for i in range(0, 9):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        header = self.MSQLTABLE_2.horizontalHeader()
        for i in range(0, 9):
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        header2 = self.MSQLTABLE_3.horizontalHeader()
        header2.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        #load init data
        self.load_data()

    # migration fields from db2 to db3
    def select_table_data(self):
        try:
            print(re.split("[, ]+", self.TEXTLINE.text()))
            numbers = sorted(list(map(int, re.split("[, ]+", self.TEXTLINE.text()))))
            result = len(numbers) == len(set(numbers)) == 3 and set(numbers).issubset(set(range(1, 9)))
            if not result:
                raise ValueError("")
            print(numbers)
            self.sqlite.delete()
            self.sqlite.create(numbers)
            self.sqlite_table_fields(numbers)
            self.sqlite_insert_data(numbers)
            self.sqlite_get_data()
        except Exception as ex:
            print(ex)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("INVALID INPUT")
            msgBox.setText("ONLY UNIQUE INTS FROM 1...8 IS AVAILABLE")
            msgBox.exec()
            self.TEXTLINE.clear()

    # set headers for db3 table
    def sqlite_table_fields(self, values):
        labels_name = [self.sqlite.table_values.get(values[0])[0], self.sqlite.table_values.get(values[1])[0],
                       self.sqlite.table_values.get(values[2])[0]]
        print(labels_name)
        self.SQLITETABLE.setRowCount(1)
        self.SQLITETABLE.setColumnCount(3)
        self.SQLITETABLE.setHorizontalHeaderLabels(labels_name)
        header = self.SQLITETABLE.horizontalHeader()
        for i in range(0, 3):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            print("FIELDS")

    # insert data to db3
    def sqlite_insert_data(self, values):
        labels_name = [self.sqlite.table_values.get(values[0])[0], self.sqlite.table_values.get(values[1])[0],
                       self.sqlite.table_values.get(values[2])[0]]
        print(labels_name)
        rows = self.postgres.select(labels_name)
        self.SQLITETABLE.setRowCount(len(rows))
        self.sqlite.insert_data(rows)

    # get data from db3
    def sqlite_get_data(self):
        data = self.sqlite.get_data()
        print("data")
        print(data)
        rows = self.SQLITETABLE.rowCount()
        columns = self.SQLITETABLE.columnCount()
        for row in range(rows):
            for column in range(columns):
                print(data[row][column])
                self.SQLITETABLE.setItem(row, column, QtWidgets.QTableWidgetItem(str(data[row][column])))

    # import data from db1 to db2
    def import_data(self):
        self.postgres.delete()
        rows = self.MSQLTABLE.rowCount()
        columns = self.MSQLTABLE.columnCount()
        for row in range(rows):
            values = list()
            for column in range(columns):
                item = self.MSQLTABLE.item(row, column)
                values.append(item.text())
            print(values)
            self.postgres.insert_data(values)
        self.load_data_postgres()

    # fill db2 table
    def load_data_postgres(self):
        values = self.postgres.print_data()
        print(values)
        self.POSTGRESTABLE.setRowCount(len(values))
        count = 0
        for value in values:
            self.POSTGRESTABLE.setItem(count, 0, QtWidgets.QTableWidgetItem(value[0]))
            self.POSTGRESTABLE.setItem(count, 1, QtWidgets.QTableWidgetItem(value[1]))
            self.POSTGRESTABLE.setItem(count, 2, QtWidgets.QTableWidgetItem(str(value[2])))
            self.POSTGRESTABLE.setItem(count, 3, QtWidgets.QTableWidgetItem(str(value[3])))
            self.POSTGRESTABLE.setItem(count, 4, QtWidgets.QTableWidgetItem(str(value[4])))
            self.POSTGRESTABLE.setItem(count, 5, QtWidgets.QTableWidgetItem(str(bool(value[5]))))
            self.POSTGRESTABLE.setItem(count, 6, QtWidgets.QTableWidgetItem(str(value[6])))
            self.POSTGRESTABLE.setItem(count, 7, QtWidgets.QTableWidgetItem(str(value[7])))
            count += 1

    # fill db1 table
    def load_data(self):
        values = self.msql.print_data()
        self.MSQLTABLE.setRowCount(len(values))
        count = 0
        for value in values:
            self.MSQLTABLE.setItem(count, 0, QtWidgets.QTableWidgetItem(value['address']))
            self.MSQLTABLE.setItem(count, 1, QtWidgets.QTableWidgetItem(value['buildingtype']))
            self.MSQLTABLE.setItem(count, 2, QtWidgets.QTableWidgetItem(str(value['apartmenttype'])))
            self.MSQLTABLE.setItem(count, 3, QtWidgets.QTableWidgetItem(str(value['square'])))
            self.MSQLTABLE.setItem(count, 4, QtWidgets.QTableWidgetItem(str(value['rooms'])))
            self.MSQLTABLE.setItem(count, 5, QtWidgets.QTableWidgetItem(str(bool(value['balcony']))))
            self.MSQLTABLE.setItem(count, 6, QtWidgets.QTableWidgetItem(str(value['floor'])))
            self.MSQLTABLE.setItem(count, 7, QtWidgets.QTableWidgetItem(str(value['price'])))
            count += 1

    # update data from db1 table to db1
    def update_table_data(self):
        rows = self.MSQLTABLE.rowCount()
        columns = self.MSQLTABLE.columnCount()
        for row in range(rows):
            values = list()
            for column in range(columns):
                item = self.MSQLTABLE.item(row, column)
                values.append(item.text())
            self.msql.update(values)
        self.load_data()

    # add data to db1
    def add_table_data(self):
        rows = self.MSQLTABLE_2.rowCount()
        columns = self.MSQLTABLE_2.columnCount()
        for row in range(rows):
            values = list()
            for column in range(columns):
                item = self.MSQLTABLE_2.item(row, column)
                if item is None:
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("SQL ERROR")
                    msgBox.setText("ALL FIELDS IS REQUIRED")
                    msgBox.exec()
                    break
                values.append(item.text())
            print(values)
            self.msql.insert_data(values)
        self.load_data()

    # delete data from db1
    def delete_table_data(self):
        val = self.MSQLTABLE_3.item(0, 0)
        if not val is None:
            print(self.MSQLTABLE_3.item(0, 0).text())
            value = self.msql.delete_data(self.MSQLTABLE_3.item(0, 0).text())
            self.msql.delete_data(str(val.text()))
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("SQL ERROR")
            msgBox.setText("FIELD IS EMPTY OR NOT SUCH ADDRESS")
            msgBox.exec()
        self.load_data()
