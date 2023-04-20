from peewee import *

from lab2.Databases.BASEMODEL import Apartment
from lab2.confings.config import MYSQL as connections

db = MySQLDatabase(
    connections.get('database'), host=connections.get("host"),
    user=connections.get("user"),
    port=connections.get("port"),
    password=connections.get("password")
)

class MysqlApartment(Apartment):
    class Meta:
        database = db
        table_name = 'apartments'


