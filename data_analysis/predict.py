import joblib 
import pandas as pd
import json
import os

import sys
sys.path.append('.')
from helper import get_latest_table
from data_analysis.preprocess import preprocess

TRAINED_MODEL_PATH = './data_analysis/results/trained_models/'

def get_latest_model():
    model_folders = os.listdir(TRAINED_MODEL_PATH)
    model_folders.sort(key=lambda x: os.path.getmtime(os.path.join(TRAINED_MODEL_PATH, x)), reverse=True)
    model_latest_folder = os.path.join(TRAINED_MODEL_PATH, model_folders[0])
    
    model_files = os.listdir(model_latest_folder)
    model_files = [f for f in model_files if f.endswith('.joblib')]
    
    model_no_gpu = joblib.load(os.path.join(model_latest_folder, 'model_no_gpu.joblib'))
    model_has_gpu = joblib.load(os.path.join(model_latest_folder, 'model_has_gpu.joblib'))
    
    return model_no_gpu, model_has_gpu
    
    

def predict(record: json) -> float:
    record = pd.DataFrame([record])
    
    cpu_specs = get_latest_table('cpu_specs')
    vga_specs = get_latest_table('gpu_specs')

    data = preprocess(record, cpu_specs, vga_specs)

    model_no_gpu, model_has_gpu = get_latest_model()
    
    if data['no_gpu'].values[0] == 1:
        return float(model_no_gpu.predict(data))
    else:
        return float(model_has_gpu.predict(data))
    
if __name__ == '__main__':
    record = {'brand': 'lenovo', 'cpu': 'aarch64', 'vga': 'firepro w5170m', 'ram_amount': 16, 'ram_type': 'ddr4', 'storage_amount': 512, 'storage_type': 'ssd', 'screen_size': 15.0, 'screen_resolution': '1366x768', 'screen_refresh_rate': 144, 'screen_brightness': 300, 'battery_capacity': 75.0, 'battery_cells': 3, 'weight': 1.5, 'width': 36.0, 'depth': 26.0, 'height': 2.5, 'number_usb_a_ports': 1, 'number_usb_c_ports': 1, 'number_hdmi_ports': 1, 'number_ethernet_ports': 1, 'number_audio_jacks': 1, 'default_os': 'Windows', 'warranty': 24, 'webcam_resolution': 'Yes'}
    print(predict(record))