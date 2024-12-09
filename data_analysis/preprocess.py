import pandas as pd 
import numpy as np
def preprocess(data: pd.DataFrame, cpu_specs: pd.DataFrame, vga_specs: pd.DataFrame) -> pd.DataFrame:
    # Merge cpu information
    columns_to_drop = ['id', 'source', 'name']
    data.drop(columns=[col for col in columns_to_drop if col in data.columns], axis=1, inplace=True)
    data = data.merge(
    cpu_specs,
    how='left',
    left_on='cpu',       # Key in the `data` DataFrame
    right_on='name',     # Key in the `cpu_specs` DataFrame
    suffixes=('', '_cpu')  # Avoid column name conflicts
    ).drop(columns=['name'])  # Optionally drop redundant key column

    # Merge GPU information
    data = data.merge(
        vga_specs,
        how='left',
        left_on='vga',       # Key in the `data` DataFrame
        right_on='name',     # Key in the `gpu_specs` DataFrame
        suffixes=('', '_gpu')  # Avoid column name conflicts
    ).drop(columns=['name'])  # Optionally drop redundant key column

    # Drop uneccessary columns
    data.drop(columns=['cpu', 
                   'vga', 
                   'number_usb_a_ports', 
                   'number_usb_c_ports',
                   'number_hdmi_ports',
                   'number_ethernet_ports',
                   'number_audio_jacks',
                   'default_os',
                   'webcam_resolution',
                   'storage_type',
                   'l1_instruction_cache',
                    'l1_data_cache',
                    'l2_cache',
                    'l3_cache',
                    'efficient_clockspeed',
                    'efficient_turbospeed',
                    'efficient_cores',
                    'efficient_threads',
                    'performance_turbospeed',
                    'eff_l1_instruction_cache',
                    'eff_l1_data_cache',
                    'eff_l2_cache',
                    'integer_math', 
                    'floating_point_math',
                    'find_prime_numbers',
                    'random_string_sorting',
                    'data_encryption',
                    'data_compression',
                    'physics',
                    'extended_instructions',
                    'bus_interface',
                    'max_memory_size',
                    'core_clock',
                    'max_direct',
                    'open_gl',
                    'test_directx_9',
                    'test_directx_10',
                    'test_directx_11',  
                    'test_directx_12',
                    'test_gpu_compute',
                    'performance_clockspeed',
                    'performance_cores', 
                    'performance_threads', 
                    'tdp',
                    'max_tdp',
                    'single_thread',
                    'single_thread_rating',
                   ], axis = 1, inplace=True)

    expected_brand_categories = ['lenovo', 'hp', 'asus', 'acer', 'dell', 'apple', 'msi', 'lg', 'gigabyte', 'microsoft']
    # Drop wrong rows 
    data.drop(data[~data['brand'].isin(expected_brand_categories)].index, inplace=True)
    data.dropna(subset=['brand'], inplace=True)
    encoded_brand = pd.get_dummies(data['brand'], prefix='brand', dtype=int).reindex(columns=[f'brand_{cat}' for cat in expected_brand_categories], fill_value=0)
    data = pd.concat([encoded_brand, data], axis=1)
    data.drop(columns=['brand'], axis = 1, inplace=True)

    expected_ram_categories = ['ddr4', 'ddr5']
    encoded_ram_type = pd.get_dummies(data['ram_type'], prefix='ram_type', dtype=int).reindex(columns=[f'ram_type_{cat}' for cat in expected_ram_categories], fill_value=0)
    data = pd.concat([encoded_ram_type, data], axis=1)
    data.drop(columns=['ram_type'], axis = 1, inplace=True)

    data['screen_area'] = data['screen_resolution'].apply(lambda x: int(x.split('x')[0])*int(x.split('x')[1]) if isinstance(x, str) else 0)
    data.drop(columns=['screen_resolution'], axis = 1, inplace=True)

    # Add attribute no_gpu 
    data['no_gpu'] = data['avg_g3d_mark'].isna().astype(int)
    # Fill missing values
    for x in data: 
        if x == 'avg_g3d_mark':
            data[x] = data[x].fillna(2684)
        
        else: 
            data[x] = data[x].fillna(data[x].mean())

    if 'price' in data.columns:
        desired_order = ['ram_type_ddr4', 'ram_type_ddr5', 'brand_acer', 'brand_asus',
        'brand_hp', 'brand_msi', 'brand_lenovo', 'brand_dell', 'brand_lg',
        'brand_gigabyte', 'brand_apple', 'brand_microsoft',
        'ram_amount', 'storage_amount', 'screen_size', 'screen_refresh_rate',
        'screen_brightness', 'battery_capacity', 'battery_cells', 'weight',
        'width', 'depth', 'height', 'warranty', 'multithread_rating',
        'no_gpu', 'avg_g3d_mark',
        'screen_area', 'price']
    
    else: 
        desired_order = ['ram_type_ddr4', 'ram_type_ddr5', 'brand_acer', 'brand_asus',
        'brand_hp', 'brand_msi', 'brand_lenovo', 'brand_dell', 'brand_lg',
        'brand_gigabyte', 'brand_apple', 'brand_microsoft', 
        'ram_amount', 'storage_amount', 'screen_size', 'screen_refresh_rate',
        'screen_brightness', 'battery_capacity', 'battery_cells', 'weight',
        'width', 'depth', 'height', 'warranty', 'multithread_rating',
        'no_gpu', 'avg_g3d_mark',
        'screen_area']
        
    data = data[desired_order]
    
    return data