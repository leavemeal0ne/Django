from peewee import *

from lab2.Databases.BASEMODEL import Apartment
from lab2.confings.config import SQLITE as connections

db = SqliteDatabase("""X:\Django\lab2\django.db""")


def create_sqlite_model(fields: [int]):
    class SqliteApartment(Model):
        class Meta:
            database = db
            table_name = 'apartments'
            primary_key = False

        @classmethod
        def get_field_names(cls):
            return [field_item.name for field_item in cls._meta.sorted_fields]
    for field in fields:
        print(Apartment.get_field_names()[field - 1])
        print(getattr(Apartment, Apartment.get_field_names()[field - 1]))
        getattr(SqliteApartment, '_meta').add_field(Apartment.get_field_names()[field - 1],
                                                    getattr(Apartment, Apartment.get_field_names()[field - 1]))
    return SqliteApartment
