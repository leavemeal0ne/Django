from peewee import *
from playhouse.shortcuts import model_to_dict

from lab2.Databases.MYSQLMODEL import *


class MYSQL:
    def __init__(self):
        db.connect()
        print(MysqlApartment.__dict__)
        db.create_tables([MysqlApartment])
        db.close()
        self.data_types = ['address', 'buildingtype', 'apartmenttype', 'square', 'rooms', 'balcony', 'floor', 'price']

    def insert_data(self, values: list):
        MysqlApartment.create(**dict(zip(self.data_types, values)))

    def print_data(self):
        items = []
        for person in MysqlApartment.select():
            items.append(model_to_dict(person))
        return items

    def update(self, values: list):
        item = dict(zip(self.data_types, values))
        MysqlApartment.update(**item).where(MysqlApartment.address == item.get('address')).execute()

    def delete(self, value):
        x = MysqlApartment.delete().where(MysqlApartment.address == value).execute()
        print(x)
        return x

