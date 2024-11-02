import pandas as pd
from typing import List

def get_create_laptop_specs_table_sql(month: int, year: int) -> str:
    """
    Return the SQL command to create a table for storing laptop specs.
    
    Args:
    - month (int): The month of the year.
    - year (int): The year.
    
    Returns:
    - str: The SQL command.
    """
    return """
        CREATE TABLE laptop_specs_{}_{} (
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
            price DECIMAL(15, 2) NOT NULL,
            width FLOAT,
            depth FLOAT,
            height FLOAT,
            number_usb_a_ports INTEGER,
            number_usb_c_ports INTEGER,
            number_hdmi_ports INTEGER,
            number_ethernet_ports INTEGER,
            number_audio_jacks INTEGER,
            PRIMARY KEY (source, name)
        );
        """.format(month, year)

def get_insert_into_laptop_specs_table_sql(csv_file_directories: List[str], month: int, year: int) -> str:
    """
    Generate SQL commands to insert data from JSON files into the laptop specs table.

    Args:
    - csv_file_directories (list): The list of JSON file directories.
    - month (int): The month of the year.
    - year (int): The year.

    Returns:
    - str: The SQL commands to insert the data.
    """
    insert_commands = []
    table_name = f"laptop_specs_{month}_{year}"

    # Process each JSON file and concatenate DataFrames
    for file_path in csv_file_directories:
        # Read the JSON file into a DataFrame
        df = pd.read_json(file_path)

        # Replace "n/a" values with None (NULL in SQL)
        df.replace("n/a", None, inplace=True)

        for _, row in df.iterrows():
            # Prepare values, substituting None for SQL NULL
            values = [
                f"'{row['source']}'" if row['source'] is not None else "NULL",
                f"'{row['brand']}'" if row['brand'] is not None else "NULL",
                f"'{row['name']}'" if row['name'] is not None else "NULL",
                f"'{row['cpu']}'" if row['cpu'] is not None else "NULL",
                f"'{row['vga']}'" if row['vga'] is not None else "NULL",
                row['ram_amount'] if row['ram_amount'] is not None else "NULL",
                f"'{row['ram_type']}'" if row['ram_type'] is not None else "NULL",
                row['storage_amount'] if row['storage_amount'] is not None else "NULL",
                f"'{row['storage_type']}'" if row['storage_type'] is not None else "NULL",
                f"'{row['webcam_resolution']}'" if row['webcam_resolution'] is not None else "NULL",
                row['screen_size'] if row['screen_size'] is not None else "NULL",
                f"'{row['screen_resolution']}'" if row['screen_resolution'] is not None else "NULL",
                row['screen_refresh_rate'] if row['screen_refresh_rate'] is not None else "NULL",
                f"'{row['screen_brightness']}'" if row['screen_brightness'] is not None else "NULL",
                row['battery_capacity'] if row['battery_capacity'] is not None else "NULL",
                row['battery_cells'] if row['battery_cells'] is not None else "NULL",
                row['weight'] if row['weight'] is not None else "NULL",
                f"'{row['default_os']}'" if row['default_os'] is not None else "NULL",
                row['warranty'] if row['warranty'] is not None else "NULL",
                # Ensure price is not NULL
                row['price'] if row['price'] is not None else "0",  # Assign a default value if needed
                row['width'] if row['width'] is not None else "NULL",
                row['depth'] if row['depth'] is not None else "NULL",
                row['height'] if row['height'] is not None else "NULL",
                row['number_usb_a_ports'] if row['number_usb_a_ports'] is not None else "NULL",
                row['number_usb_c_ports'] if row['number_usb_c_ports'] is not None else "NULL",
                row['number_hdmi_ports'] if row['number_hdmi_ports'] is not None else "NULL",
                row['number_ethernet_ports'] if row['number_ethernet_ports'] is not None else "NULL",
                row['number_audio_jacks'] if row['number_audio_jacks'] is not None else "NULL"
            ]

            # Join the values into a comma-separated string
            values_str = ", ".join(map(str, values))

            insert_command = f"""
            INSERT INTO {table_name} (
                source, brand, name, cpu, vga, ram_amount, ram_type, 
                storage_amount, storage_type, webcam_resolution, screen_size, 
                screen_resolution, screen_refresh_rate, screen_brightness, 
                battery_capacity, battery_cells, weight, default_os, 
                warranty, price, width, depth, height, 
                number_usb_a_ports, number_usb_c_ports, number_hdmi_ports, 
                number_ethernet_ports, number_audio_jacks
            ) VALUES (
                {values_str}
            );"""
            insert_commands.append(insert_command.strip())

    return "\n".join(insert_commands)