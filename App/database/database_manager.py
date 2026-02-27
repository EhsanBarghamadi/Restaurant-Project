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

class SuperDatabaseManager():
    def __init__(self):
            try:
                check_list = [os.getenv("DEFAULT_NAME"), os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT")]
                if None in check_list:
                    logging.error("Problem connecting to database and .env file")
                    self.value_check = False
                else:
                    self.DEFAULT_NAME = os.getenv("DEFAULT_NAME")
                    self.NEW_DB_NAME = os.getenv("NEW_DB_NAME")
                    self.DB_USERNAME = os.getenv("DB_USERNAME")
                    self.__DB_PASSWORD = os.getenv("DB_PASSWORD")
                    self.DB_HOST = os.getenv("DB_HOST")
                    self.DB_PORT = os.getenv("DB_PORT")
                    self.value_check = True
            except ValueError as error:
                logging.error(f"The database input values ​​are invalid.\nError: {error}")
                raise ValueError
    
    def create_database(self) -> tuple[bool, str]:
        if not self.value_check:
            return False, "Problem connecting to the database"
        conn = None
        try:
            conn = psycopg2.connect(
                database=self.DEFAULT_NAME,
                user=self.DB_USERNAME,
                password=self.__DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT
            )
            logging.info("Connection to database was successful.")
            conn.autocommit = True
            query = f"CREATE DATABASE {self.NEW_DB_NAME};"
            with conn.cursor() as cur:
                cur.execute(query)
                return True, f"Database {self.NEW_DB_NAME} addition completed successfully."
        except Exception as e:
            return False, f"Error Database: {e}"
        finally:
            if conn:
                conn.close()

class DatabaseManager():
    """
    A helper class to handle PostgreSQL operations using psycopg2.
    Supports query execution, data fetching, and SQL script running.
    """
    
    def __init__(self):
            try:
                check_list = [os.getenv("NEW_DB_NAME"), os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT")]
                if None in check_list:
                    logging.error("Problem connecting to database and .env file")
                    self.value_check = False
                else:
                    self.NEW_DB_NAME = os.getenv("NEW_DB_NAME")
                    self.DB_USERNAME = os.getenv("DB_USERNAME")
                    self.__DB_PASSWORD = os.getenv("DB_PASSWORD")
                    self.DB_HOST = os.getenv("DB_HOST")
                    self.DB_PORT = os.getenv("DB_PORT")
                    self.value_check = True
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

    def get_connect(self) -> tuple[bool , object | str]:
        if not self.value_check:
            return False, "Problem connecting to the database"
        try:
            conn = psycopg2.connect(
                database=self.NEW_DB_NAME,
                user=self.DB_USERNAME,
                password=self.__DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT
            )
            logging.info("Connection to database was successful.")
            return True, conn
        except Exception as er:
            return False, f"Database Error: {er}"

    def query_tool(self, query: str, params:tuple | list[tuple] = None, conn=None, execute_many=False, fetch_one=False, fetch_all=False, end=True) -> tuple:
        own_connection = False
        if conn is None:
                    result, conn = self.get_connect()
                    if not result:
                        logging.error(f"Connection Error: {conn}")
                        return False, f"Connection Error: {conn}"
                    own_connection = True        
        try:
            with conn.cursor() as cur:
                if execute_many:
                    cur.executemany(query, params)
                else:
                    cur.execute(query, params)
                data = None
                if fetch_one:
                    data = cur.fetchone()
                elif fetch_all:
                    data = cur.fetchall()
                if end:
                    conn.commit()
                if fetch_one or fetch_all:
                    return True, data
                return True, "Operation successful."
                
        except Exception as error:
            end = True
            conn.rollback()
            logging.error(error)
            return False, f"Query Error: {error}"
        
        finally:
            if own_connection and end and conn:
                            conn.close()


    def run_script_file(self, file_script:str) -> bool:
        """Function related to creating tables and triggers with file address"""
        try:
            with open(file_script , "r", encoding="utf-8") as file:
                scripts = file.read()
                result, message = self.query_tool(scripts)
                if not result:
                    print(f"Error executing statement: {message}")
                    return False
                return True
        except Exception as error:
            logging.error(f"Message Error: {error}")
            return False, f"Message Error: {error}"

