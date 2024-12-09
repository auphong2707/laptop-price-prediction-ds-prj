import joblib 
import pandas as pd
import json
import os

import sys
sys.path.append('.')
from helper import get_latest_table
from data_analysis.preprocess import preprocess

def predict(record: json) -> float:
    record = pd.DataFrame([record])
    # print(record)
    cpu_specs = get_latest_table('cpu_specs')
    vga_specs = get_latest_table('gpu_specs')

    # cpu_specs = pd.read_csv('/home/quangminh/Documents/code/Python/ProjectDS/laptop-price-prediction-ds-prj/data_analysis/data/cpu_specs_11_2024.csv')
    # vga_specs = pd.read_csv('/home/quangminh/Documents/code/Python/ProjectDS/laptop-price-prediction-ds-prj/data_analysis/data/gpu_specs_11_2024.csv')
    data = preprocess(record, cpu_specs, vga_specs)
    model_folder = '/home/quangminh/Documents/code/Python/ProjectDS/laptop-price-prediction-ds-prj/data_analysis/results/stored_model'

    model_possible_name = os.listdir(model_folder)
    if data['no_gpu'][0] == 1:
        model_possible_name = [f for f in model_possible_name if 'non_gaming' in f]
    else:   
        model_possible_name = [f for f in model_possible_name if 'gaming' in f]
    model_files = [f for f in model_possible_name if f.endswith('.joblib')]
    model_files.sort(key=lambda x: os.path.getmtime(os.path.join(model_folder, x)), reverse=True)
    last_model = os.path.join(model_folder, model_files[0])
    
    model = joblib.load(last_model)

    return float(model.predict(data))

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--data', type=str, help='The path to the data')
    # args = parser.parse_args()
    # Code to get record, cpu_specs, vga_specs
    record = {'brand': 'lenovo', 'cpu': 'aarch64', 'vga': 'firepro w5170m', 'ram_amount': 16, 'ram_type': 'ddr4', 'storage_amount': 512, 'storage_type': 'ssd', 'screen_size': 15.0, 'screen_resolution': '1366x768', 'screen_refresh_rate': 144, 'screen_brightness': 300, 'battery_capacity': 75.0, 'battery_cells': 3, 'weight': 1.5, 'width': 36.0, 'depth': 26.0, 'height': 2.5, 'number_usb_a_ports': 1, 'number_usb_c_ports': 1, 'number_hdmi_ports': 1, 'number_ethernet_ports': 1, 'number_audio_jacks': 1, 'default_os': 'Windows', 'warranty': 24, 'webcam_resolution': 'Yes'}
    print(predict(record))