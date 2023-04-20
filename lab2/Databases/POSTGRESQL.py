from peewee import *
from playhouse.shortcuts import model_to_dict
from lab2.Databases.POSTGRESQLMODEL import *


class POSTGRESQL:
    def __init__(self):
        db.connect()
        db.create_tables([PostgresqlApartment])
        db.close()
        self.data_types = ['address', 'buildingtype', 'apartmenttype', 'square', 'rooms', 'balcony', 'floor', 'price']

    def insert_data(self, values: list):
        PostgresqlApartment.create(**dict(zip(self.data_types, values)))

    def print_data(self):
        items = []
        for person in PostgresqlApartment.select():
            items.append(model_to_dict(person))
        return items

    def update(self, values: list):
        item = dict(zip(self.data_types, values))
        PostgresqlApartment.update(**item).where(PostgresqlApartment.address == item.get('address')).execute()

    def delete(self, value):
        x = PostgresqlApartment.delete().where(PostgresqlApartment.address == value).execute()
        return x

    def select(self, values:list[str]):
        new_list = []
        for d in self.print_data():
            new_dict = {}
            for k, v in d.items():
                if k in values:
                    new_dict[k] = v
            new_list.append(new_dict)
        return new_list
    def delete_all(self):
        PostgresqlApartment.delete().execute()


