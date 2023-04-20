from peewee import *


class Apartment(Model):
    address = CharField(max_length=50, primary_key=True)
    buildingtype = CharField(max_length=50)
    apartmenttype = CharField(max_length=50)
    square = FloatField()
    rooms = IntegerField()
    balcony = BooleanField()
    floor = IntegerField()
    price = FloatField()

    @classmethod
    def get_field_names(cls):
        return [field_item.name for field_item in cls._meta.sorted_fields]


