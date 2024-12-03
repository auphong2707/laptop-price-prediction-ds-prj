import psycopg2
import pandas as pd

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

def get_full_relation(month: int, year: int) -> pd.DataFrame:
    # Connect to the database
    connection = _connect_to_postgres()
    
    # Query the database
    query = f"""
        SELECT 
            ls.*,
            cs.*,
            gs.*
        FROM 
            laptop_specs_{month}_{year} AS ls
        LEFT JOIN 
            cpu_specs_{month}_{year} AS cs
        ON 
            ls.cpu = cs.name
        LEFT JOIN 
            gpu_specs_{month}_{year} AS gs
        ON 
            ls.vga = gs.name;
    """
    
    # Execute the query
    result = connection.cursor()
    result.execute(query)
    
    # Fetch the result
    df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
    
    # Add prefix the laptop_specs columns
    for i in range(len(df.columns)):
        if i <= len(LAPTOP_SPECS_COLUMNS):
            df.rename(columns={df.columns[i]: f'laptop_specs_{df.columns[i]}'}, inplace=True)
        elif i <= len(LAPTOP_SPECS_COLUMNS) + len(CPU_SPECS_COLUMNS):
            df.rename(columns={df.columns[i]: f'cpu_specs_{df.columns[i]}'}, inplace=True)
        else:
            df.rename(columns={df.columns[i]: f'gpu_specs_{df.columns[i]}'}, inplace=True)

    # Close the connection
    connection.close()
    
    return df

def get_cpu_table(month: int, year: int) -> pd.DataFrame:
    # Connect to the database
    connection = _connect_to_postgres()
    
    # Query the database
    query = f"""
        SELECT 
            *
        FROM 
            cpu_specs_{month}_{year};
    """
    
    # Execute the query
    result = connection.cursor()
    result.execute(query)
    
    # Fetch the result
    df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
    
    # Close the connection
    connection.close()
    
    return df

def get_gpu_table(month: int, year: int) -> pd.DataFrame:
    # Connect to the database
    connection = _connect_to_postgres()
    
    # Query the database
    query = f"""
        SELECT 
            *
        FROM 
            gpu_specs_{month}_{year};
    """
    
    # Execute the query
    result = connection.cursor()
    result.execute(query)
    
    # Fetch the result
    df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
    
    # Close the connection
    connection.close()
    
    return df

def get_laptop_table(month: int, year: int) -> pd.DataFrame:
    # Connect to the database
    connection = _connect_to_postgres()
    
    # Query the database
    query = f"""
        SELECT 
            *
        FROM 
            laptop_specs_{month}_{year};
    """
    
    # Execute the query
    result = connection.cursor()
    result.execute(query)
    
    # Fetch the result
    df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
    
    # Close the connection
    connection.close()
    
    return df

if __name__ == '__main__':
    import os
    os.makedirs('./data_analysis/data', exist_ok=True)
    
    df = get_full_relation(11, 2024)
    df.to_csv('./data_analysis/data/full_relation_11_2024.csv', index=False)
    
    df = get_laptop_table(11, 2024)
    df.to_csv('./data_analysis/data/laptop_specs_11_2024.csv', index=False)
    
    df = get_cpu_table(11, 2024)
    df.to_csv('./data_analysis/data/cpu_specs_11_2024.csv', index=False)
    
    df = get_gpu_table(11, 2024)
    df.to_csv('./data_analysis/data/gpu_specs_11_2024.csv', index=False)