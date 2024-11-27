import json
import psycopg2
from airflow.utils.dates import timezone
from decimal import Decimal
import os

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


def _check_integrity(conn: psycopg2.extensions.connection,
                    checking_type: str,
                    table_name: str,
                    tmp_data_path: str,
                    export_path: str):
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM {}".format(table_name))
    
    records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    formatted_records = []
    for record in records:
        formatted_record = {}
        for col_name, value in zip(column_names, record):
            # Skip 'id' column
            if col_name == 'id':
                continue

            # Replace None (NULL in SQL) with 'n/a'
            if value is None:
                formatted_record[col_name] = 'n/a'

            # Convert Decimal to float
            elif isinstance(value, Decimal):
                formatted_record[col_name] = float(value)
            else:
                formatted_record[col_name] = value
        
        formatted_records.append(formatted_record)
    records = formatted_records
    
    tmp_data = json.load(open(tmp_data_path))
    for row in tmp_data:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.replace("'", "").replace('"', "")
    
    # CHEKCING INTEGRITY
    checking_results = "CHECKING RESULT OF {}:\n".format(checking_type)
    
    # Checking number of records in JSON file and database
    checking_results += '\n' + '-'*50 + '\n'
    checking_results += "Checking number of records in JSON file and database\n"
    
    checking_results += f"Number of records in JSON file: {len(tmp_data)}\n"
    checking_results += f"Number of records in database: {len(records)}\n"
    
    if len(tmp_data) != len(records):
        checking_results += "\nNumber of records in JSON file and database do not match\n"
    else:
        checking_results += "\nNumber of records in JSON file and database match\n"
    checking_results += '-'*50 + '\n'
    
    
    # Checking if all records in JSON file are in database
    checking_results += '\n' + '-'*50 + '\n'
    checking_results += "Checking if all records in JSON file are in database\n"
    unmatched_records = []
    
    for i, record in enumerate(tmp_data):
        checking_results += f"Checking record {i+1}: "
        if record in records:
            checking_results += "Matched\n"
        else:
            checking_results += "Unmatched\n"
            unmatched_records.append(record)
    
    if len(unmatched_records) > 0:
        checking_results += f"\nUnmatched records:\n"
        for record in unmatched_records:
            checking_results += f"{record}\n"
    else:
        checking_results += "All records in JSON file are in database\n"
    checking_results += '-'*50 + '\n'
    
    # Checking if all records in database are in JSON file
    checking_results += '\n' + '-'*50 + '\n'
    checking_results += "Checking if all records in database are in JSON file\n"
    unmatched_records = []
    
    for i, record in enumerate(records):
        checking_results += f"Checking record {i+1}: "
        if record in tmp_data:
            checking_results += "Matched\n"
        else:
            checking_results += "Unmatched\n"
            unmatched_records.append(record)
    
    if len(unmatched_records) > 0:
        checking_results += f"\nUnmatched records:\n"
        for record in unmatched_records:
            checking_results += f"{record}\n"
    else:
        checking_results += "All records in database are in JSON file\n"
    checking_results += '-'*50 + '\n'
    
    # Ensure the directory for export_path exists
    export_dir = os.path.dirname(export_path)
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    with open(export_path, 'w') as file:
        file.write(checking_results)

def _combine_json_files(json_files: list, combined_json_path: str):
    combined_json = []
    for json_file in json_files:
        data = json.load(open(json_file))
        combined_json.extend(data)
    with open(combined_json_path, 'w') as file:
        json.dump(combined_json, file)

def check_integrity_all():
    conn = _connect_to_postgres()
    print(__file__)

    _check_integrity(conn, 
                    'CPU', 
                    'cpu_specs_{}_{}'.format(timezone.utcnow().month, timezone.utcnow().year), 
                    './temp/cpu_data.json', 
                    './logs/database/cpu_integrity_check_result.log')
    
    _check_integrity(conn, 
                    'GPU', 
                    'gpu_specs_{}_{}'.format(timezone.utcnow().month, timezone.utcnow().year), 
                    './temp/gpu_data.json', 
                    './logs/database/gpu_integrity_check_result.log')
    
    laptop_shops = [
        'gearvn',
        'cellphones',
        'fptshop',
        'hacom',
        'laptopaz',
        'laptopworld',
        'nguyenkim',
        'phongvu',
        'phucanh',
        'tgdd'
    ]
    _combine_json_files(['./temp/' + laptop_shop + '_data.json' for laptop_shop in laptop_shops], 
                        './temp/laptop_data.json')
    
    _check_integrity(conn, 
                    'LAPTOP', 
                    'laptop_specs_{}_{}'.format(timezone.utcnow().month, timezone.utcnow().year), 
                    './temp/laptop_data.json', 
                    './logs/database/laptop_integrity_check_result.log')
