import psycopg2

class DatabaseManager():
    """
    A helper class to handle PostgreSQL operations using psycopg2.
    Supports query execution, data fetching, and SQL script running.
    """
    
    def __init__(self, user_db, pass_db, host_db='127.0.0.1', port_db='5432'):
        self.NAME_DB = 'restarant_db'
        self.user_db = user_db
        self.__pass_db = pass_db
        self.host_db = host_db
        self.port_db = port_db

    @property
    def pass_db(self):
        print("Unable to view password")
        return None

    @pass_db.setter
    def pass_db(self, value):
        self.__pass_db = value

    def connect(self) -> tuple[bool , object | str]:
        try:
            conn = psycopg2.connect(
                database=self.NAME_DB,
                user=self.user_db,
                password=self.__pass_db,
                host=self.host_db,
                port=self.port_db
            )
            return True, conn
        except Exception as error:
            return False, error

    def query_tool(self, query, params=None, fetch=False):
        result, conn = self.connect()
        if not result:
            return False, f"Connection Error: {conn}"
        
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return True, cur.fetchall()
                else:
                    conn.commit()
                    return True, "Operation successful."

        except Exception as error:
            conn.rollback()
            return False, f"Query Error: {error}"
        finally:
            conn.close()

    def run_script_file(self, file_script):
        try:
            with open(file_script , "r", encoding="utf-8") as file:
                scripts = file.read()
            result, massage = self.query_tool(scripts)
            if result:
                return True
            else:
                return False
            
        except Exception as error:
            return False, f"Massage Error: {error}"

