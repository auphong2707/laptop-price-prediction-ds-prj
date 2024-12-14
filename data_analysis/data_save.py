import datetime
import sys
import os

sys.path.append('.')
from helper import get_latest_table

MONTH = datetime.datetime.now().month
YEAR = datetime.datetime.now().year
SAVE_DIRECTORY = f'./data_analysis/data/{MONTH}_{YEAR}'
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

def save_data_as_csv():
    cpu_specs = get_latest_table('cpu_specs')
    gpu_specs = get_latest_table('gpu_specs')
    laptop_specs = get_latest_table('laptop_specs')
    
    full_relational_data = get_latest_table('full_relation')
    
    cpu_specs.to_csv(f'{SAVE_DIRECTORY}/cpu_specs.csv', index=False)
    gpu_specs.to_csv(f'{SAVE_DIRECTORY}/gpu_specs.csv', index=False)
    laptop_specs.to_csv(f'{SAVE_DIRECTORY}/laptop_specs.csv', index=False)
    full_relational_data.to_csv(f'{SAVE_DIRECTORY}/full_relational_data.csv', index=False)
    
if __name__ == '__main__':
    save_data_as_csv()