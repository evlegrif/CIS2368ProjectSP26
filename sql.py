import mysql.connector
from mysql.connector import Error

def create_connection(hostname,username,userpw,dbname):
    connection = None
    try: 
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=userpw,
            database=dbname
        )
        print("connection successful")   #good idea to add a note to see if and error shows up
    except Error as e:
        print(f'the error {e} occured')
    return connection

def execute_query(connection, query):       # execute this without getting anything back
    cursor = connection.cursor()           # go to the database and check this information to confirm it exist on the db
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f'the error {e} occured')

def execute_read_query(connection, query):            # execute this but you will get something back
    cursor = connection.cursor(dictionary = True)
    result = None

    try: 
        cursor.execute(query)
        result = cursor.fetchall()
        return result    
    except Error as e:
        print(f'the error {e} occured')
