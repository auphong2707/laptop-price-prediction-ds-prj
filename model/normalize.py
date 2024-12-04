import pandas as pd
from sklearn.preprocessing import MinMaxScaler
def normalize(data: pd.DataFrame) -> pd.DataFrame: 
    data = data.drop(['screen_area', 'screen_ratio', 'gpu_specs_test_directx_9', 'gpu_specs_test_directx_11', 'gpu_specs_test_directx_12'], axis=1)
    def encode_with_nearest(value):
        if value in categories:
            return categories[value]
        else:
            nearest_key = min(categories.keys(), key=lambda k: abs(k - value))
            return categories[nearest_key]
    
    categories = {
        4.0: 0,
        8.0: 1,
        12.0: 2,
        16.0: 4,
        18.0: 5,
        24.0: 6,
        32.0: 7,
        48.0: 8,
        96.0: 9,
        }

    data['laptop_specs_ram_amount'] = data['laptop_specs_ram_amount'].apply(encode_with_nearest)

    categories ={
        256.0: 0,
        512.0: 1,
        1024.0: 2,
        2048.0: 3
    }
    data['laptop_specs_storage_amount'] = data['laptop_specs_storage_amount'].apply(encode_with_nearest)

    categories = {
        12.0: 0, 
        18.0: 1,
        24.0: 2, 
        36.0: 3
        }
    data['laptop_specs_warranty'] = data['laptop_specs_warranty'].apply(encode_with_nearest)

    categories = {
        60.0: 0, 
        90.0: 1,
        120.0: 2, 
        144.0: 3, 
        165.0: 4, 
        180.0: 5, 
        240.0: 6, 
        360.0:7
    }
    data['laptop_specs_screen_refresh_rate'] = data['laptop_specs_screen_refresh_rate'].apply(encode_with_nearest)

    data['laptop_specs_screen_size'] = data['laptop_specs_screen_size']/15.6
    data['laptop_specs_battery_cells'] = data['laptop_specs_battery_cells']/3

    scaler = MinMaxScaler()

    data['laptop_specs_screen_brightness'] = scaler.fit_transform(data['laptop_specs_screen_brightness'].to_frame()) + 0.1
    data['laptop_specs_battery_capacity'] = scaler.fit_transform(data['laptop_specs_battery_capacity'].to_frame()) + 0.1
    data['cpu_specs_multithread_rating'] = scaler.fit_transform(data['cpu_specs_multithread_rating'].to_frame()) + 0.1
    data['cpu_specs_single_thread_rating'] = scaler.fit_transform(data['cpu_specs_single_thread_rating'].to_frame()) + 0.1
    data['cpu_specs_data_compression'] = scaler.fit_transform(data['cpu_specs_data_compression'].to_frame()) + 0.1
    data['cpu_specs_integer_math'] = scaler.fit_transform(data['cpu_specs_integer_math'].to_frame()) + 0.1
    data['cpu_specs_floating_point_math'] = scaler.fit_transform(data['cpu_specs_floating_point_math'].to_frame()) + 0.1
    data['cpu_specs_find_prime_numbers'] = scaler.fit_transform(data['cpu_specs_find_prime_numbers'].to_frame()) + 0.1
    data['cpu_specs_random_string_sorting'] = scaler.fit_transform(data['cpu_specs_random_string_sorting'].to_frame()) + 0.1
    data['cpu_specs_data_encryption'] = scaler.fit_transform(data['cpu_specs_data_encryption'].to_frame()) + 0.1
    data['cpu_specs_physics'] = scaler.fit_transform(data['cpu_specs_physics'].to_frame()) + 0.1
    data['cpu_specs_single_thread'] = scaler.fit_transform(data['cpu_specs_single_thread'].to_frame()) + 0.1
    data['cpu_specs_extended_instructions'] = scaler.fit_transform(data['cpu_specs_extended_instructions'].to_frame()) + 0.1
    data['gpu_specs_avg_g3d_mark'] = scaler.fit_transform(data['gpu_specs_avg_g3d_mark'].to_frame())
    data['gpu_specs_test_directx_10'] = scaler.fit_transform(data['gpu_specs_test_directx_10'].to_frame())
    data['gpu_specs_test_gpu_compute'] = scaler.fit_transform(data['gpu_specs_test_gpu_compute'].to_frame())

    return data

# data = pd.read_csv('/home/quangminh/Documents/code/Python/ProjectDS/laptop-price-prediction-ds-prj/train_processed.csv')
# X = data.drop('laptop_specs_price', axis=1)
# print(normalize(X).describe())