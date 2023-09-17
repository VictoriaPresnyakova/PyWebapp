import psycopg2
from psycopg2 import Error


class SQLError(Exception):
    pass


class ConnectionError(Exception):
    pass


class UseDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self) -> psycopg2.connect:
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(**self.configuration)

            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
            #connection.commit()
        except psycopg2.OperationalError as error:
            raise ConnectionError(error)

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Соединение с PostgreSQL закрыто")
        if exc_type:
            raise SQLError(exc_type)
