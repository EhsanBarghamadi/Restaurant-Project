from dotenv import load_dotenv
import os
import psycopg2
import logging
load_dotenv()

logging.basicConfig(
    filename='database.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DatabaseManager():
    """
    A helper class to handle PostgreSQL operations using psycopg2.
    Supports query execution, data fetching, and SQL script running.
    """
    
    def __init__(self):
            try:
                check_list = [os.getenv("DB_NAME"), os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT")]
                if None in check_list:
                    logging.error("Problem connecting to database and .env file")
                    self.check = False
                else:
                    self.DB_NAME = os.getenv("DB_NAME")
                    self.DB_USERNAME = os.getenv("DB_USERNAME")
                    self.__DB_PASSWORD = os.getenv("DB_PASSWORD")
                    self.DB_HOST = os.getenv("DB_HOST")
                    self.DB_PORT = os.getenv("DB_PORT")
                    self.check = True
            except ValueError as error:
                logging.error(f"The database input values ​​are invalid.\nError: {error}")
                raise ValueError

    @property
    def DB_PASSWORD(self):
        print("Unable to view password")
        return None
    
    @DB_PASSWORD.setter
    def DB_PASSWORD(self, value):
        self.__DB_PASSWORD = value

    def connect(self) -> tuple[bool , object | str]:
        if not self.check:
            return False, "Problem connecting to the database"
        conn = psycopg2.connect(
            database=self.DB_NAME,
            user=self.DB_USERNAME,
            password=self.__DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        logging.info("Connection to database was successful.")
        return True, conn

    def query_tool(self, query, params=None, fetch=False, number=False) -> tuple[bool , object | str]:
        result, conn = self.connect()
        if not result:
            logging.error(f"Connection Error: {conn}")
            return False, f"Connection Error: {conn}"
        try:
            with conn.cursor() as cur:
                if not number:
                    cur.execute(query, params)
                if number:
                    cur.executemany(query, params)
                if fetch:
                    return True, cur.fetchall()
                else:
                    conn.commit()
                    return True, "Operation successful."
        except Exception as error:
            conn.rollback()
            logging.error(error)
            return False, f"Query Error: {error}"
        finally:
            conn.close()

    def run_script_file(self, file_script) -> bool:
        try:
            with open(file_script , "r", encoding="utf-8") as file:
                scripts = file.read()
            result, message = self.query_tool(scripts)
            if result:
                return True
            else:
                return False
        except Exception as error:
            logging.error(f"Message Error: {error}")
            return False, f"Message Error: {error}"

