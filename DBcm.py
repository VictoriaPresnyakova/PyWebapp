import psycopg2
from psycopg2 import Error


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
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Соединение с PostgreSQL закрыто")
