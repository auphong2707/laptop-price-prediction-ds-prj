import pandas as pd
import psycopg2

def _connect_to_postgres(dbname='airflow', user='airflow', password='airflow', host='localhost', port='5432'):
    try:
        # Establish the connection
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except Exception as error:
        print(f"Error: {error}")
        return None

def get_table_list():
    conn = _connect_to_postgres()
    cursor = conn.cursor()
    
    # Query the database
    query = """
        SELECT schemaname, tablename
        FROM pg_tables
        WHERE tablename LIKE '%_specs_%';
    """
    
    cursor.execute(query)
    tables = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return [table[1] for table in tables]

def get_table(table_name) -> pd.DataFrame:
    conn = _connect_to_postgres()
    result = conn.cursor()
    
    # Query the database
    query = f"""
        SELECT *
        FROM {table_name};
    """
    
    result.execute(query)

    # Change the data to a DataFrame
    table = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
    
    # Close the connection
    conn.close()
    
    return table

def get_latest_table(table_name) -> pd.DataFrame:
    table_names = get_table_list()
    
    filtered_table_names = [name for name in table_names if table_name in name]
    lastest_table_name = sorted(filtered_table_names)[-1]
    
    return get_table(lastest_table_name)