from dotenv import load_dotenv
import psycopg2
import os
load_dotenv()

def get_connection():
    '''
    This function is for connecting to the database.
    '''
    value = [os.getenv("DB_NAME"),
            os.getenv("DB_USERNAME"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT")]
    if None in value:
        print("Please define the variables in the env file correctly.(referral .env.example)")
        return None
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return connection
    
    except Exception as error:
        print(f"Error in connection:\n {error}")
        return None

def manager_connection(fun):
    def wrapper(*args, **kwargs):
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                result = fun(cur, *args, **kwargs)
                conn.commit()
                return result
            
            except Exception as error:
                conn.rollback()
                print(f"Error: {error}")
                
            finally:
                cur.close()
                conn.close()
    return wrapper