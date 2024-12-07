import joblib 
import pandas as pd
from preprocess import preprocess
import argparse
import json

def predict(record: json, cpu_specs, vga_specs) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument('--model_path', type=str, help='The path to the model')
    model = joblib.load(parser.model_path)
    # cpu_specs = pd.read_csv(cpu_specs)
    # vga_specs = pd.read_csv(vga_specs)

    record = pd.read_json(record)
    data = preprocess(record, cpu_specs, vga_specs)
    return model.predict(data)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--data', type=str, help='The path to the data')
    # args = parser.parse_args()
    # Code to get record, cpu_specs, vga_specs
    record = None
    cpu_specs = None
    vga_specs = None
    # predict
    predict(record, cpu_specs, vga_specs)