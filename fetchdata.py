# fetchdata.py

import sys
import mysql.connector
import pandas as pd

def connect_to_mysql(username, password, database, host):
    conn = mysql.connector.connect(
        user=username,
        password=password,
        database=database,
        host=host
    )
    return conn

def read_data_into_dataframe(conn, table_name):
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql_query(query, conn)
    return df

def get_row_by_id(conn, table_name, user_id):
    cursor = conn.cursor(dictionary=True)

    try:
        query = f'SELECT * FROM {table_name} WHERE student_id = %s'
        cursor.execute(query, (user_id,))
        result_row = cursor.fetchall()

        if result_row:
            return result_row
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: fetchdata.py <user_id> <database_choice>")
        sys.exit(1)

    user_id = sys.argv[1]
    database_choice = sys.argv[2]

    databases = {
        'student': {'username': 'root', 'password': '10thLo94%', 'database': 'student', 'host': 'localhost'},
        'employee': {'username': 'root', 'password': '10thLo94%', 'database': 'employee', 'host': 'localhost'},
        'research': {'username': 'root', 'password': '10thLo94%', 'database': 'research', 'host': 'localhost'},
        'economic_growth': {'username': 'root', 'password': '10thLo94%', 'database': 'economic_growth', 'host': 'localhost'},
    }

    selected_database = database_choice.lower()

    # Connect to the selected MySQL database
    conn = connect_to_mysql(**databases[selected_database])

    # Map database names to their corresponding table names
    table_name_mapping = {
        'student': 'students',
        'employee': 'employees',
        'research': 'research_articles',
        'economic_growth': 'economic_growth'
    }

    # Read data into Pandas DataFrame
    table_name = table_name_mapping[selected_database]

    result_row = get_row_by_id(conn, table_name, user_id)

    if result_row is not None:
        print(result_row)
    else:
        print(f"No entry found for ID: {user_id}")

    # Close the MySQL connection
    conn.close()

if __name__ == "__main__":
    main()
