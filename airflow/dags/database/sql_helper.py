import json
from typing import List

# [LAPTOPS]
def get_create_laptop_specs_table_sql(month: int, year: int) -> str:
    """
    Return the SQL command to create a table for storing laptop specs.
    
    Args:
    - month (int): The month of the year.
    - year (int): The year.
    
    Returns:
    - str: The SQL command.
    """
    return f"""
        CREATE TABLE laptop_specs_{month}_{year} (
            source VARCHAR(255) NOT NULL,
            brand VARCHAR(255),
            name VARCHAR(255) NOT NULL,
            cpu VARCHAR(255),
            vga VARCHAR(255),
            ram_amount INTEGER,
            ram_type VARCHAR(50),
            storage_amount INTEGER,
            storage_type VARCHAR(50),
            webcam_resolution VARCHAR(50),
            screen_size FLOAT,
            screen_resolution VARCHAR(50),
            screen_refresh_rate INTEGER,
            screen_brightness VARCHAR(50),
            battery_capacity FLOAT,
            battery_cells INTEGER,
            weight FLOAT,
            default_os VARCHAR(255),
            warranty INTEGER,
            price INT NOT NULL,
            width FLOAT,
            depth FLOAT,
            height FLOAT,
            number_usb_a_ports INTEGER,
            number_usb_c_ports INTEGER,
            number_hdmi_ports INTEGER,
            number_ethernet_ports INTEGER,
            number_audio_jacks INTEGER,
            PRIMARY KEY (source, name),
            FOREIGN KEY (cpu) REFERENCES cpu_specs_{month}_{year}(name),
            FOREIGN KEY (vga) REFERENCES gpu_specs_{month}_{year}(name)
        );
        """

def get_insert_into_laptop_specs_table_sql(json_file_directories: List[str], month: int, year: int) -> str:
    """
    Generate SQL commands to insert data from JSON files into the laptop specs table.

    Args:
    - json_file_directories (list): The list of JSON file directories.
    - month (int): The month of the year.
    - year (int): The year.

    Returns:
    - str: The SQL commands to insert the data.
    """
    insert_commands = []
    laptop_table_name = f"laptop_specs_{month}_{year}"
    cpu_table_name = f"cpu_specs_{month}_{year}"
    gpu_table_name = f"gpu_specs_{month}_{year}"

    # Process each JSON file
    for file_path in json_file_directories:
        # Load JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Iterate through the list of records in the JSON data
        for row in data:
            # Replace "n/a" with None
            for key, value in row.items():
                if value == "n/a":
                    row[key] = None

            # Filter out records that don't have a price
            if row.get('price') is None:
                continue  # Skip this record if price is not present
            
            # Strip quotes from all string values
            for key, value in row.items():
                if isinstance(value, str):
                    row[key] = value.strip("'\"")

            # Prepare values, substituting None for SQL NULL
            values = [
                f"'{row['source']}'" if row.get('source') is not None else "NULL",
                f"'{row['brand']}'" if row.get('brand') is not None else "NULL",
                f"'{row['name']}'" if row.get('name') is not None else "NULL",
                f"'{row['cpu']}'" if row.get('cpu') is not None else "NULL",
                f"'{row['vga']}'" if row.get('vga') is not None else "NULL",
                row.get('ram_amount') if row.get('ram_amount') is not None else "NULL",
                f"'{row['ram_type']}'" if row.get('ram_type') is not None else "NULL",
                row.get('storage_amount') if row.get('storage_amount') is not None else "NULL",
                f"'{row['storage_type']}'" if row.get('storage_type') is not None else "NULL",
                f"'{row['webcam_resolution']}'" if row.get('webcam_resolution') is not None else "NULL",
                row.get('screen_size') if row.get('screen_size') is not None else "NULL",
                f"'{row['screen_resolution']}'" if row.get('screen_resolution') is not None else "NULL",
                row.get('screen_refresh_rate') if row.get('screen_refresh_rate') is not None else "NULL",
                f"'{row['screen_brightness']}'" if row.get('screen_brightness') is not None else "NULL",
                row.get('battery_capacity') if row.get('battery_capacity') is not None else "NULL",
                row.get('battery_cells') if row.get('battery_cells') is not None else "NULL",
                row.get('weight') if row.get('weight') is not None else "NULL",
                f"'{row['default_os']}'" if row.get('default_os') is not None else "NULL",
                row.get('warranty') if row.get('warranty') is not None else "NULL",
                row.get('price'),
                row.get('width') if row.get('width') is not None else "NULL",
                row.get('depth') if row.get('depth') is not None else "NULL",
                row.get('height') if row.get('height') is not None else "NULL",
                row.get('number_usb_a_ports') if row.get('number_usb_a_ports') is not None else "NULL",
                row.get('number_usb_c_ports') if row.get('number_usb_c_ports') is not None else "NULL",
                row.get('number_hdmi_ports') if row.get('number_hdmi_ports') is not None else "NULL",
                row.get('number_ethernet_ports') if row.get('number_ethernet_ports') is not None else "NULL",
                row.get('number_audio_jacks') if row.get('number_audio_jacks') is not None else "NULL"
            ]

            # Join the values into a comma-separated string
            values_str = ", ".join(map(str, values))

            # Create the insert command with conditional logic
            insert_command = f"""
            INSERT INTO {laptop_table_name} (
                source, brand, name, cpu, vga, ram_amount, ram_type, 
                storage_amount, storage_type, webcam_resolution, screen_size, 
                screen_resolution, screen_refresh_rate, screen_brightness, 
                battery_capacity, battery_cells, weight, default_os, 
                warranty, price, width, depth, height, 
                number_usb_a_ports, number_usb_c_ports, number_hdmi_ports, 
                number_ethernet_ports, number_audio_jacks
            ) 
            SELECT {values_str} 
            WHERE EXISTS (SELECT 1 FROM {cpu_table_name} WHERE name = {values[3]})
            {("AND EXISTS (SELECT 1 FROM {} WHERE name = " + str(values[4]) + ")").format(gpu_table_name) if values[4] != "NULL" else ""}
            ON CONFLICT (source, name) DO NOTHING;
            """
            insert_commands.append(insert_command.strip())

    return "\n".join(insert_commands)


# [CPUs]
def get_create_cpu_specs_table_sql(month: int, year: int) -> str:
    """
    Return the SQL command to create a table for storing CPU specs.
    
    Args:
    - month (int): The month of the year.
    - year (int): The year.
    
    Returns:
    - str: The SQL command.
    """
    return """
        CREATE TABLE cpu_specs_{}_{} (
            name VARCHAR(255) PRIMARY KEY,
            performance_clockspeed DECIMAL(4, 2),
            performance_turbospeed DECIMAL(4, 2),
            performance_cores INT,
            performance_threads INT,
            efficient_clockspeed DECIMAL(4, 2),
            efficient_turbospeed DECIMAL(4, 2),
            efficient_cores INT,
            efficient_threads INT,
            tdp DECIMAL(5, 2),
            multithread_rating INT,
            single_thread_rating INT,
            l1_instruction_cache VARCHAR(20),
            l1_data_cache VARCHAR(20),
            l2_cache VARCHAR(20),
            l3_cache VARCHAR(20),
            eff_l1_instruction_cache VARCHAR(20),
            eff_l1_data_cache VARCHAR(20),
            eff_l2_cache VARCHAR(20),
            integer_math INT,
            floating_point_math INT,
            find_prime_numbers INT,
            random_string_sorting INT,
            data_encryption INT,
            data_compression INT,
            physics INT,
            extended_instructions INT,
            single_thread INT
        );
        """.format(month, year)

def get_insert_into_cpu_specs_table_sql(json_file_directory: str, month: int, year: int) -> str:
    """
    Generate SQL commands to insert data from a JSON file into the cpu_specs table.

    Args:
    - json_file_directory (str): The path to the JSON file.

    Returns:
    - str: The SQL commands to insert the data.
    """
    insert_commands = []
    table_name = f"cpu_specs_{month}_{year}"

    # Load the JSON file
    with open(json_file_directory) as f:
        cpu_data = json.load(f)

    for cpu in cpu_data:
        # Prepare values, substituting 'n/a' for SQL NULL
        values = [
            f"'{cpu['name']}'" if cpu.get('name') != "n/a" else "NULL",
            cpu.get('performance_clockspeed', "NULL") if cpu.get('performance_clockspeed') != "n/a" else "NULL",
            cpu.get('performance_turbospeed', "NULL") if cpu.get('performance_turbospeed') != "n/a" else "NULL",
            cpu.get('performance_cores', "NULL") if cpu.get('performance_cores') != "n/a" else "NULL",
            cpu.get('performance_threads', "NULL") if cpu.get('performance_threads') != "n/a" else "NULL",
            cpu.get('efficient_clockspeed', "NULL") if cpu.get('efficient_clockspeed') != "n/a" else "NULL",
            cpu.get('efficient_turbospeed', "NULL") if cpu.get('efficient_turbospeed') != "n/a" else "NULL",
            cpu.get('efficient_cores', "NULL") if cpu.get('efficient_cores') != "n/a" else "NULL",
            cpu.get('efficient_threads', "NULL") if cpu.get('efficient_threads') != "n/a" else "NULL",
            cpu.get('tdp', "NULL") if cpu.get('tdp') != "n/a" else "NULL",
            cpu.get('multithread_rating', "NULL") if cpu.get('multithread_rating') != "n/a" else "NULL",
            cpu.get('single_thread_rating', "NULL") if cpu.get('single_thread_rating') != "n/a" else "NULL",
            f"'{cpu['l1_instruction_cache']}'" if cpu.get('l1_instruction_cache') != "n/a" else "NULL",
            f"'{cpu['l1_data_cache']}'" if cpu.get('l1_data_cache') != "n/a" else "NULL",
            f"'{cpu['l2_cache']}'" if cpu.get('l2_cache') != "n/a" else "NULL",
            f"'{cpu['l3_cache']}'" if cpu.get('l3_cache') != "n/a" else "NULL",
            f"'{cpu['eff_l1_instruction_cache']}'" if cpu.get('eff_l1_instruction_cache') != "n/a" else "NULL",
            f"'{cpu['eff_l1_data_cache']}'" if cpu.get('eff_l1_data_cache') != "n/a" else "NULL",
            f"'{cpu['eff_l2_cache']}'" if cpu.get('eff_l2_cache') != "n/a" else "NULL",
            cpu.get('integer_math', "NULL") if cpu.get('integer_math') != "n/a" else "NULL",
            cpu.get('floating_point_math', "NULL") if cpu.get('floating_point_math') != "n/a" else "NULL",
            cpu.get('find_prime_numbers', "NULL") if cpu.get('find_prime_numbers') != "n/a" else "NULL",
            cpu.get('random_string_sorting', "NULL") if cpu.get('random_string_sorting') != "n/a" else "NULL",
            cpu.get('data_encryption', "NULL") if cpu.get('data_encryption') != "n/a" else "NULL",
            cpu.get('data_compression', "NULL") if cpu.get('data_compression') != "n/a" else "NULL",
            cpu.get('physics', "NULL") if cpu.get('physics') != "n/a" else "NULL",
            cpu.get('extended_instructions', "NULL") if cpu.get('extended_instructions') != "n/a" else "NULL",
            cpu.get('single_thread', "NULL") if cpu.get('single_thread') != "n/a" else "NULL"
        ]

        # Join the values into a comma-separated string
        values_str = ", ".join(map(str, values))

        insert_command = f"""
        INSERT INTO {table_name} (
            name, performance_clockspeed, performance_turbospeed, performance_cores, performance_threads,
            efficient_clockspeed, efficient_turbospeed, efficient_cores, efficient_threads,
            tdp, multithread_rating, single_thread_rating,
            l1_instruction_cache, l1_data_cache, l2_cache, l3_cache,
            eff_l1_instruction_cache, eff_l1_data_cache, eff_l2_cache,
            integer_math, floating_point_math, find_prime_numbers,
            random_string_sorting, data_encryption, data_compression,
            physics, extended_instructions, single_thread
        ) VALUES (
            {values_str}
        )
        ON CONFLICT (name) DO UPDATE SET
            name = CONCAT(EXCLUDED.name, ' (duplicate ', (
                SELECT COUNT(*) FROM {table_name} AS tbl WHERE tbl.name LIKE EXCLUDED.name || ' (duplicate %)'
            ) + 1, ')'),
            performance_clockspeed = EXCLUDED.performance_clockspeed,
            performance_turbospeed = EXCLUDED.performance_turbospeed,
            performance_cores = EXCLUDED.performance_cores,
            performance_threads = EXCLUDED.performance_threads,
            efficient_clockspeed = EXCLUDED.efficient_clockspeed,
            efficient_turbospeed = EXCLUDED.efficient_turbospeed,
            efficient_cores = EXCLUDED.efficient_cores,
            efficient_threads = EXCLUDED.efficient_threads,
            tdp = EXCLUDED.tdp,
            multithread_rating = EXCLUDED.multithread_rating,
            single_thread_rating = EXCLUDED.single_thread_rating,
            l1_instruction_cache = EXCLUDED.l1_instruction_cache,
            l1_data_cache = EXCLUDED.l1_data_cache,
            l2_cache = EXCLUDED.l2_cache,
            l3_cache = EXCLUDED.l3_cache,
            eff_l1_instruction_cache = EXCLUDED.eff_l1_instruction_cache,
            eff_l1_data_cache = EXCLUDED.eff_l1_data_cache,
            eff_l2_cache = EXCLUDED.eff_l2_cache,
            integer_math = EXCLUDED.integer_math,
            floating_point_math = EXCLUDED.floating_point_math,
            find_prime_numbers = EXCLUDED.find_prime_numbers,
            random_string_sorting = EXCLUDED.random_string_sorting,
            data_encryption = EXCLUDED.data_encryption,
            data_compression = EXCLUDED.data_compression,
            physics = EXCLUDED.physics,
            extended_instructions = EXCLUDED.extended_instructions,
            single_thread = EXCLUDED.single_thread;
        """
        insert_commands.append(insert_command.strip())

    return "\n".join(insert_commands)
        
# [GPUs]
def get_create_gpu_specs_table_sql(month: int, year: int) -> str:
    """
    Return the SQL command to create a table for storing GPU specs.
    
    Args:
    - month (int): The month of the year.
    - year (int): The year.
    
    Returns:
    - str: The SQL command.
    """
    return """
        CREATE TABLE gpu_specs_{}_{} (
            name VARCHAR(255) PRIMARY KEY NOT NULL,
            avg_g3d_mark INT,
            bus_interface VARCHAR(50),
            max_memory_size INT,
            core_clock INT,
            max_direct VARCHAR(10),
            open_gl DECIMAL(3, 1),
            max_tdp INT,
            test_directx_9 INT,
            test_directx_10 INT,
            test_directx_11 INT,
            test_directx_12 INT,
            test_gpu_compute INT
        );
        """.format(month, year)

def get_insert_into_gpu_specs_table_sql(json_file_directory: str, month: int, year: int) -> str:
    """
    Generate SQL commands to insert data from a JSON file into the gpu_specs table.

    Args:
    - json_file_directory (str): The path to the JSON file.

    Returns:
    - str: The SQL commands to insert the data.
    """
    insert_commands = []
    table_name = f"gpu_specs_{month}_{year}"

    # Load the JSON file
    with open(json_file_directory) as f:
        gpu_data = json.load(f)

    for gpu in gpu_data:
        # Prepare values, substituting 'n/a' for SQL NULL
        values = [
            f"'{gpu['name']}'" if gpu.get('name') != "n/a" else "NULL",
            gpu.get('avg_g3d_mark', "NULL"),
            f"'{gpu['bus_interface']}'" if gpu.get('bus_interface') != "n/a" else "NULL",
            gpu.get('max_memory_size', "NULL") if gpu.get('max_memory_size') != "n/a" else "NULL",
            gpu.get('core_clock', "NULL") if gpu.get('core_clock') != "n/a" else "NULL",
            f"'{gpu['max_direct']}'" if gpu.get('max_direct') != "n/a" else "NULL",
            gpu.get('open_gl', "NULL") if gpu.get('open_gl') != "n/a" else "NULL",
            gpu.get('max_tdp', "NULL") if gpu.get('max_tdp') != "n/a" else "NULL",
            gpu.get('test_directx_9', "NULL") if gpu.get('test_directx_9') != "n/a" else "NULL",
            gpu.get('test_directx_10', "NULL") if gpu.get('test_directx_10') != "n/a" else "NULL",
            gpu.get('test_directx_11', "NULL") if gpu.get('test_directx_11') != "n/a" else "NULL",
            gpu.get('test_directx_12', "NULL") if gpu.get('test_directx_12') != "n/a" else "NULL",
            gpu.get('test_gpu_compute', "NULL") if gpu.get('test_gpu_compute') != "n/a" else "NULL"
        ]

        # Join the values into a comma-separated string
        values_str = ", ".join(map(str, values))

        insert_command = f"""
        INSERT INTO {table_name} (
            name, avg_g3d_mark, bus_interface, max_memory_size, core_clock,
            max_direct, open_gl, max_tdp, test_directx_9, test_directx_10,
            test_directx_11, test_directx_12, test_gpu_compute
        ) VALUES (
            {values_str}
        )
        ON CONFLICT (name) DO UPDATE SET
            name = CONCAT(EXCLUDED.name, ' (duplicate ', (
                SELECT COUNT(*) FROM {table_name} AS tbl WHERE tbl.name LIKE EXCLUDED.name || ' (duplicate %)'
            ) + 1, ')'),
            avg_g3d_mark = EXCLUDED.avg_g3d_mark,
            bus_interface = EXCLUDED.bus_interface,
            max_memory_size = EXCLUDED.max_memory_size,
            core_clock = EXCLUDED.core_clock,
            max_direct = EXCLUDED.max_direct,
            open_gl = EXCLUDED.open_gl,
            max_tdp = EXCLUDED.max_tdp,
            test_directx_9 = EXCLUDED.test_directx_9,
            test_directx_10 = EXCLUDED.test_directx_10,
            test_directx_11 = EXCLUDED.test_directx_11,
            test_directx_12 = EXCLUDED.test_directx_12,
            test_gpu_compute = EXCLUDED.test_gpu_compute;
        """
        insert_commands.append(insert_command.strip())

    return "\n".join(insert_commands)
