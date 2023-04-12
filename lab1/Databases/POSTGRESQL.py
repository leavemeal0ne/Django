from lab1.confings.config import POSTGRESQL as connections
import psycopg2


# class to work with postgres db

class POSTGRESQL:
    def __init__(self):
        self.host = connections.get("host")
        self.user = connections.get("user")
        self.port = connections.get("port")
        self.password = connections.get("password")
        self.database = connections.get("database")

    #insert data in db
    def insert_data(self, val):
        try:
            print(self.database)
            conn = psycopg2.connect(dbname=self.database, user=self.user, password=self.password, host=self.host,
                                    port=self.port)
            print("Successfully connected")
            with conn.cursor() as cursor:
                sql = "INSERT INTO apartments (address, buildingtype, apartmenttype ,square, rooms, " \
                      "balcony " \
                      ", floor ,price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
                cursor.execute(sql, val)
                conn.commit()
            conn.close()
        except Exception as ex:
            print("error")
            print(ex)

    # get data from db
    def print_data(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            print("Successfully connected")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM apartments")
                    rows = cursor.fetchall()
                    print(rows)
                    return rows
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    # delete data from db
    def delete(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            print("Successfully connected")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM apartments")
                    connection.commit()
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    # custom select from db
    def select(self, values):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            print("Successfully connected")
            try:
                with connection.cursor() as cursor:
                    print(values)
                    cursor.execute(f'SELECT {values[0]}, {values[1]}, {values[2]} FROM apartments')
                    rows = cursor.fetchall()
                    return rows
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)
