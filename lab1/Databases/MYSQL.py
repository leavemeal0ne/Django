import pymysql.cursors

from lab1.confings.config import MYSQL as connections


# class to work with mysql

class MYSQL:
    def __init__(self):
        self.host = connections.get("host")
        self.user = connections.get("user")
        self.port = connections.get("port")
        self.password = connections.get("password")
        self.database = connections.get("database")

    # insert data to db
    def insert_data(self, val):
        try:
            connection_msql = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Successfully connected")
            try:
                with connection_msql.cursor() as cursor:
                    sql = "INSERT INTO `apartments` (`address`, `buildingtype`, `apartmenttype` ,`square`, `rooms`, " \
                          "`balcony` " \
                          ", `floor` ,`price`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
                    cursor.execute(sql, (val[0], val[1], val[2], val[3], val[4], bool(val[5]), val[6], val[7]))
                    connection_msql.commit()
            finally:
                connection_msql.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    # get data from db
    def print_data(self):
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Successfully connected")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM `apartments`")
                    rows = cursor.fetchall()
                    return rows
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    # delete data from db
    def delete_data(self, val1):
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Successfully connected")
            try:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `apartments` WHERE `address`=%s"
                    cursor.execute(sql, val1)
                    connection.commit()
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    # update data in db
    def update(self, ls):
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Successfully connected")
            try:
                floor = None
                if str(ls[5]).lower() in ["true", "y", "1"]:
                    floor = 1
                else:
                    floor = 0
                with connection.cursor() as cursor:
                    sql = "Update `apartments` set `address`=%s, `buildingtype`=%s, `apartmenttype`=%s, `square`=%s, " \
                          "`rooms`=%s, `balcony`=%s," \
                          " `floor`=%s, `price` =%s WHERE `address`=%s"
                    cursor.execute(sql, (ls[0], ls[1], ls[2], ls[3], ls[4], floor, ls[6], ls[7], ls[0]))
                    connection.commit()
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused...")
            print(ex)
