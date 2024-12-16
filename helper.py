import pandas as pd
import psycopg2

LAPTOP_SPECS_COLUMNS = [
    "id", "source", "brand", "name", "cpu", "vga", "ram_amount", "ram_type", 
    "storage_amount", "storage_type", "webcam_resolution", "screen_size", 
    "screen_resolution", "screen_refresh_rate", "screen_brightness", 
    "battery_capacity", "battery_cells", "weight", "default_os", "warranty", 
    "price", "width", "depth", "height", "number_usb_a_ports", 
    "number_usb_c_ports", "number_hdmi_ports", "number_ethernet_ports", 
    "number_audio_jacks"
]

CPU_SPECS_COLUMNS = [
    "name", "performance_clockspeed", "performance_turbospeed", "performance_cores", "performance_threads",
    "efficient_clockspeed", "efficient_turbospeed", "efficient_cores", "efficient_threads", "tdp",
    "multithread_rating", "single_thread_rating", "l1_instruction_cache", "l1_data_cache", "l2_cache", "l3_cache",
    "eff_l1_instruction_cache", "eff_l1_data_cache", "eff_l2_cache", "integer_math", "floating_point_math",
    "find_prime_numbers", "random_string_sorting", "data_encryption", "data_compression", "physics",
    "extended_instructions", "single_thread"
]

GPU_SPECS_COLUMNS = [
    "name", "avg_g3d_mark", "bus_interface", "max_memory_size", "core_clock", "max_direct", "open_gl", 
    "max_tdp", "test_directx_9", "test_directx_10", "test_directx_11", "test_directx_12", "test_gpu_compute"
]

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
    if len(table_names) == 0:
        return None
    
    if table_name == 'full_relation':
        laptop_table = [name for name in table_names if 'laptop_specs' in name][-1]
        cpu_table = [name for name in table_names if 'cpu_specs' in name][-1]
        gpu_table = [name for name in table_names if 'gpu_specs' in name][-1]
        
        conn = _connect_to_postgres()
        # Query the database
        query = f"""
            SELECT 
                ls.*,
                cs.*,
                gs.*
            FROM 
                {laptop_table} AS ls
            LEFT JOIN 
                {cpu_table} AS cs
            ON 
                ls.cpu = cs.name
            LEFT JOIN 
                {gpu_table} AS gs
            ON 
                ls.vga = gs.name;
        """
        
        # Execute the query
        result = conn.cursor()
        result.execute(query)
        
        # Fetch the result
        df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
            
        # Initialize a set to track renamed columns
        renamed_columns = set()

        def make_unique(column_name, counter=1):
            """Ensure column names are unique by appending a counter if needed."""
            unique_name = column_name
            while unique_name in renamed_columns:
                unique_name = f"{column_name}_{counter}"
                counter += 1
            renamed_columns.add(unique_name)
            return unique_name

        # Prepare a list to store the new column names
        new_column_names = []

        # Iterate through the columns and generate new column names
        for i, col in enumerate(df.columns):
            if i < len(LAPTOP_SPECS_COLUMNS):
                new_name = f'laptop_specs_{col}'
            elif i < len(LAPTOP_SPECS_COLUMNS) + len(CPU_SPECS_COLUMNS):
                new_name = f'cpu_specs_{col}'
            else:
                new_name = f'gpu_specs_{col}'

            # Make the column name unique
            unique_name = make_unique(new_name)
            new_column_names.append(unique_name)

        # Assign the new column names to the DataFrame at once
        df.columns = new_column_names

        # Close the connection
        conn.close()

        return df
    else:
        filtered_table_names = [name for name in table_names if table_name in name]
        lastest_table_name = sorted(filtered_table_names)[-1]
    
    return get_table(lastest_table_name)