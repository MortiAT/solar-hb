import psycopg2
import time
import os

class DatabaseAccess:
    def __init__(self):
        self.__db_config = {
            "host": "timescale",
            "port": 5432,
            "database": os.getenv('POSTGRES_DB'),
            "user": os.getenv('POSTGRES_USER'),
            "password": os.getenv('POSTGRES_PASSWORD')
        }
        self.__conn = self.__connect()

    def __connect(self):
        return psycopg2.connect(**self.__db_config)
    
    def insert(self, values: dict):
        while True:
            try:
                with self.__conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO sensor_data (time, p_akku, p_grid, p_load, p_pv, relative_charge)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        values["time"],
                        values["p_akku"],
                        values["p_grid"],
                        values["p_load"],
                        values["p_pv"],
                        values["relative_charge"]
                    ))
                    self.__conn.commit()
                    return

            except psycopg2.OperationalError:
                self.__conn.close()
                self.__conn = self.__connect()

            time.sleep(300)