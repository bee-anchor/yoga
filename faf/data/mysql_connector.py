import pymysql
import pymysql.cursors


class MySQLConnector:

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def _create_connection(self):
        return pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.password,
                               db=self.db,
                               cursorclass=pymysql.cursors.DictCursor)

    def query(self, sql, args=()):

        connection = self._create_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)

            connection.commit()

        finally:
            connection.close()

    def query_return_all_results(self, sql, args=()):

        connection = self._create_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                return cursor.fetchall()

        finally:
            connection.close()

    def query_return_one_result(self, sql, args=()):

        connection = self._create_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                return cursor.fetchone()

        finally:
            connection.close()
