import re
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QHeaderView, QMessageBox

from lab2.Databases.BASEMODEL import Apartment
from lab2.Databases.POSTGRESQL import POSTGRESQL
from lab2.Databases.MYSQL import MYSQL
from lab2.Databases.SQLITE import SQLITE


# main window class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("Main.ui", self)

        # add objects to work with DBC
        self.msql = MYSQL()
        self.postgres = POSTGRESQL()
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
            self.sqlite.init(numbers)
            self.sqlite_table_fields(numbers)
            self.sqlite_insert_data(numbers)
            self.sqlite_get_data(numbers)
        except Exception as ex:
            self.show_msg([f'INVALID INPUT", "ONLY UNIQUE INTS FROM 1...8 IS AVAILABLE {ex}'])
            self.TEXTLINE.clear()

    # set headers for db3 table
    def sqlite_table_fields(self, values):
        labels_name = [Apartment.get_field_names()[values[0] - 1], Apartment.get_field_names()[values[1] - 1],
                       Apartment.get_field_names()[values[2] - 1]]
        print(labels_name)
        self.SQLITETABLE.setRowCount(1)
        self.SQLITETABLE.setColumnCount(3)
        self.SQLITETABLE.setHorizontalHeaderLabels(labels_name)
        header = self.SQLITETABLE.horizontalHeader()
        for i in range(0, 3):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    # insert data to db3
    def sqlite_insert_data(self, values):
        labels_name = [Apartment.get_field_names()[values[0] - 1], Apartment.get_field_names()[values[1] - 1],
                       Apartment.get_field_names()[values[2] - 1]]

        rows = self.postgres.select(labels_name)
        self.sqlite.insert_data_from_dict(rows)

    # get data from db3
    def sqlite_get_data(self, numbers):
        values = self.sqlite.print_data()
        print("XD")
        print(values)
        if values is not None:
            self.SQLITETABLE.setRowCount(len(values))
            row = 0
            for value in values:
                for (column, field) in zip(range(0, 3), [Apartment.get_field_names()[numbers[0] - 1],
                                                         Apartment.get_field_names()[numbers[1] - 1],
                                                         Apartment.get_field_names()[numbers[2] - 1]]):
                    self.SQLITETABLE.setItem(row, column, QtWidgets.QTableWidgetItem(str(value.get(field))))
                row += 1

    # import data from db1 to db2
    def import_data(self):
        self.postgres.delete_all()
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
        if values is not None:
            self.POSTGRESTABLE.setRowCount(len(values))
            row = 0
            for value in values:
                for (column, field) in zip(range(0, 8), self.postgres.data_types):
                    self.POSTGRESTABLE.setItem(row, column, QtWidgets.QTableWidgetItem(str(value.get(field))))
                row += 1

    # fill db1 table
    def load_data(self):
        values = self.msql.print_data()
        if values is not None:
            self.MSQLTABLE.setRowCount(len(values))
            row = 0
            for value in values:
                for (column, field) in zip(range(0, 8), self.msql.data_types):
                    self.MSQLTABLE.setItem(row, column, QtWidgets.QTableWidgetItem(str(value.get(field))))
                row += 1

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
                    self.show_msg(["SQL ERROR", "ALL FIELDS IS REQUIRED"])
                    return
                values.append(item.text())
            print(values)
            try:
                self.msql.insert_data(values)
            except Exception as ex:
                self.show_msg(["SQL ERROR", f'Duplicate value "address" {ex}'])
        self.load_data()

    # delete data from db1
    def delete_table_data(self):
        val = self.MSQLTABLE_3.item(0, 0)
        if val is not None:
            value = self.msql.delete(self.MSQLTABLE_3.item(0, 0).text())
            if value == 0:
                self.show_msg(["SQL ERROR", "NOT SUCH ADDRESS"])
        else:
            self.show_msg(["SQL ERROR", "FIELD IS EMPTY"])
        self.load_data()

    def show_msg(self, value):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(value[0])
        msgBox.setText(value[1])
        msgBox.exec()
