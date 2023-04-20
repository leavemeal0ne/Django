from peewee import *
from playhouse.shortcuts import model_to_dict

from lab2.Databases.SQLITEMODEL import *


class SQLITE:
    def __init__(self):
        self.db = db
        self.SqliteApartment = None
        self.data_types = ['address', 'buildingtype', 'apartmenttype', 'square', 'rooms', 'balcony', 'floor', 'price']

    def init(self, fields: [int]):
        self.SqliteApartment = create_sqlite_model(fields)
        print(self.SqliteApartment.get_field_names())
        self.db.drop_tables([self.SqliteApartment])
        self.db.create_tables([self.SqliteApartment])
        db.close()

    def insert_data(self, values: list):
        self.SqliteApartment.create(**dict(zip(self.data_types, values)))

    def insert_data_from_dict(self, values):
        for value in values:
            self.SqliteApartment.create(**value)

    def print_data(self):
        items = []
        for person in self.SqliteApartment.select():
            items.append(model_to_dict(person))
        return items

    def update(self, values: list):
        item = dict(zip(self.data_types, values))
        self.SqliteApartment.update(**item).where(self.SqliteApartment.address == item.get('address')).execute()

    def delete(self, value):
        x = self.SqliteApartment.delete().where(self.SqliteApartment.address == value).execute()
        return x

    def delete_all(self):
        print(self.SqliteApartment.delete().execute())
