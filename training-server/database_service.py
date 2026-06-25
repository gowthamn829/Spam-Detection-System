import psycopg2


class DatabaseService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.connection = psycopg2.connect(
                host="localhost",
                port="5432",
                database="trainingdb",
                user="postgres",
                password="1234"
            )

        return cls._instance

    def get_connection(self):

        return self.connection


database_service = DatabaseService()