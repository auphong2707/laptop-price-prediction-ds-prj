# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
import pprint


class ScraperPipeline:
    def process_item(self, item, spider):
        return item

class TransformPipeline:
    def process_item(self, item, spider):    
        # Convert the item to a more accessible object using ItemAdapter
        adapter = ItemAdapter(item)
        
        self.convert_to_lowercase(adapter)
        self.strip_whitespace(adapter)
        
        if getattr(spider, 'require_specific_transform', True):
            pass
        else:
            self.GeneralTransformer(adapter).transform_all()

        return item

    def convert_to_lowercase(self, adapter: ItemAdapter):
        """Converts all fields to lowercase."""
        for field_name, value in adapter.items():
            if isinstance(value, str):
                adapter[field_name] = value.lower()
                
    def strip_whitespace(self, adapter: ItemAdapter):
        """Strips leading and trailing whitespace from all fields."""
        for field_name, value in adapter.items():
            if isinstance(value, str):
                adapter[field_name] = value.strip()
                
    class GeneralTransformer:
        def __init__(self, adapter: ItemAdapter):
            self.adapter = adapter
            self.debug_mode = False

        def transform_cpu(self):
            """Transforms the CPU field to a standardized format."""
            try:
                # Get the CPU field value
                value = self.adapter.get('cpu')
                if value == "n/a":
                    return
                
                # Basic cleaning steps
                for removal in ['®', '™', ' processors', ' processor', 'mobile',
                                'with intel ai boost', '', '(tm)', '(r)', ':',
                                'tiger lake', 'ice lake', 'raptor lake', 'alder lake', 
                                'comet lake', 'kabylake refresh', 'kabylake', 'cpu']:
                    value = value.replace(removal, '')
                    
                special_sep = re.search(r'\b(\d+\.\d+\s?upto\s?\d+\.\d+ghz|\d+(\.\d+)?\s*ghz|\d+\s?gb|dgb)\b', value)
                if special_sep:
                    value = value.split(special_sep.group())[0]
                
                for spliter in [',',  'up']:
                    value = value.split(spliter)[0]
                
                value = ' '.join(value.split()).strip()
                
                # Apple solving
                if self.adapter.get('brand') == "apple":
                    cpu_name = re.search(r'm\d+(\s+pro|\s+max)?', value, re.IGNORECASE)
                    if cpu_name:
                        # Update the pattern to be more general for core counting and fix the encoding issue
                        pattern = re.compile(r'(\d+)\s*(lõi|nhân|core|-core)', re.IGNORECASE)
                        num_cores = pattern.search(value)
                        if num_cores:
                            num_cores = num_cores.group(1)  # The number of cores will be in the first group
                            value = f"apple {cpu_name.group(0)} {num_cores}-core"
                        else:
                            value = f"apple {cpu_name.group(0)}"
                else:
                    value = re.sub(r'\([^()]*\)', '', value)
                    
                    # Intel solving
                    if any(keyword in value for keyword in ['i5', 'i7', 'i9', 'i3']):
                        
                        pattern = re.compile(r'(i\d)\s*[- ]?\s*(\d{4,5})([a-z]{0,2})')
                        match = pattern.search(value)
                    
                        if match:
                            # Format the matched processor name as "iX-XXXXXH"
                            value = 'intel core ' + f"{match.group(1)}-{match.group(2)}{match.group(3)}"
                        else:
                            value = "n/a"
                    elif "ultra" in value:
                        pattern = re.compile(r'(?:ultra\s*)?(u?\d)\s*[- ]?\s*(\d{3})([a-z]?)')
                        match = pattern.search(value)
                        
                        if match:
                            model_number = match.group(1).replace('u', '')
                            value = 'intel core ' + f"ultra {model_number} {match.group(2)}{match.group(3)}"
                    
                    # AMD solving
                    elif "ryzen" in value:
                        pattern = re.compile(r'(?:ryzen\s*)?(\d)\s*[- ]?\s*(\d{4})([a-z]{0,2})')
                        
                        match = pattern.search(value)
                        
                        if match:
                            value = 'amd ' f"ryzen {match.group(1)} {match.group(2)}{match.group(3)}"
                            
                    elif "amd" in value:
                        # pattern = re.compile(r'(amd)\s*([a-z]{3,4})\s*(\d{3,4})')
                        
                        # match = pattern.search(value)
                        
                        # if match:
                        #     value = 'amd ' + f"{match.group(2)} {match.group(3)}"
                        pass
                            
                    # Snapdragon solving
                    elif "snapdragon" in value:
                        pattern = r'([A-Za-z]+\s+\d+\s+\d+)'
                        
                        # Define a function to replace spaces with hyphens in the matched string
                        def replace_with_hyphens(match):
                            # Split the matched string into components and join with hyphens
                            components = match.group(0).split()
                            return '-'.join(components)
                        
                        # Substitute the pattern in the input string using re.sub
                        value = re.sub(pattern, replace_with_hyphens, value)
                        
                    
                        
                value = value.split('(')[0].split('(')[0].strip()
                    
                self.adapter['cpu'] = value
            except Exception as e:
                print("Error in CPU transformation:", e)
                print("Error at:", self.adapter.get('name'))
            
        def transform_vga(self):
            try:
                # Get the VGA field value
                value = self.adapter.get('vga')
                if value == "n/a":
                    return
                
                # Basic cleaning steps
                value = re.sub(r'[^\x20-\x7E]|®|™|integrated|gpu', ' ', value, flags=re.IGNORECASE)              
                value = re.sub(r'\([^()]*\)', '', value)
                
                special_sep = re.search(r'\d+\s?gb|gddr\d+|\d+g', value)
                if special_sep:
                    value = value.split(special_sep.group())[0]
                
                for spliter in [' with ', ' laptop ', '+', ',',  'up', 'upto', 'up to', 'rog']:
                    value = value.split(spliter)[0]
                
                value = ' '.join(value.split())

                # Apple solving
                if self.adapter.get('brand') == "apple":
                    value = 'n/a'
                else:
                    if any([keyword in value for keyword in ['nvidia', 'geforce', 'rtx', 'gtx']]):
                        for removal in ['amd radeon graphics', 'intel uhd graphics', 'laptop', 'nvidia',
                                        'intel iris xe', 'graphics', 'vga:', 'vga - ', ':']:
                            value = value.replace(removal, '')
                            value = ' '.join(value.split())
                        
                        if (value.startswith('rtx') and 'ada' not in value) \
                           or value.startswith('gtx'):
                            value = 'geforce ' + value
                            
                        value = re.sub(r'(\s\d{3,4})ti', r'\1 ti', value)
                        value = re.sub(r'(tx)(\d{4})', r'\1 \2', value)
                        
                        if 'geforce' in value:
                            value = value[value.index('geforce'):]
                        
                    elif any([keyword in value for keyword in ['iris xe', 'intel uhd', 'intel hd', 'intel graphics', 
                                                               'intel arc', 'adreno', 'onboard', 'on board', 'uma',]]):
                        value = "n/a"
                    elif any([keyword in value for keyword in ['amd', 'radeon']]):
                        value = value.replace('amd', '')
                        
                        if 'vega' in value:
                            value = "n/a"
                        elif not 'rx' in value:
                            value = "n/a"
                    
                value = value.strip()
                
                self.adapter['vga'] = value
            except Exception as e:
                print("Error in VGA transformation:", e)
                print("Error at:", self.adapter.get('name'))
            
        def transform_ram_amount(self):
            """Transforms the RAM amount field to a standardized format."""
            try:
                # Get the RAM amount field value
                value = self.adapter.get('ram_amount')
                if value == "n/a":
                    return
                
                search_value = re.search(r'\d+\s?gb', value)
                if search_value:
                    value = search_value.group()
                    value = int(value.split('gb')[0])
                elif self.adapter.get('source') == 'hacom' and re.search(r'\d+\s?g', value):
                    value = re.search(r'\d+\s?g', value).group()
                    value = int(value.split('g')[0])
                else:
                    pass    
                    
                self.adapter['ram_amount'] = value
            except Exception as e:
                print("Error in RAM amount transformation:", e)
                print("Error at:", self.adapter.get('name'))
            
        def transform_ram_type(self):
            """Transforms the RAM type field to a standardized format."""
            try:
                # Get the RAM type field value
                value = self.adapter.get('ram_type')
                if value == "n/a":
                    return
                search_value = re.search(r'ddr+\d', value)
                if search_value:
                    value = search_value.group()
                elif '3200' in value:
                    value = 'ddr4'
                # else: 
                #     value = "n/a"
                
                self.adapter['ram_type'] = value
            except Exception as e:
                print("Error in RAM type transformation:", e)
                print("Error at:", self.adapter.get('name'))
            
        def transform_storage_amount(self):
            """Transforms the storage amount field to a standardized format."""
            try:
                # Get the storage amount field value
                value = self.adapter.get('storage_amount')
                if value == "n/a":
                    return
                
                value = ''.join(value.split())
                
                search_value = re.search(r'\d+gb|\d+tb', value)
                if search_value:
                    value = search_value.group()
                    if 'tb' in value:
                        value = int(value.split('tb')[0]) * 1024
                    else:
                        value = int(value.split('gb')[0])
                
                self.adapter['storage_amount'] = value
            except Exception as e:
                print("Error in storage amount transformation:", e)
                print("Error at:", self.adapter.get('name'))
            
        def transform_storage_type(self):
            """Transforms the storage type field to a standardized format."""
            try:
                # Get the storage type field value
                value = self.adapter.get('storage_type')
                if value == "n/a":
                    return
                
                if any(x in value for x in ["ssd", "pcie"]) and "hdd" in value:
                    if min(value.index(x) for x in ["ssd", "pcie"] if x in value) < value.index("hdd"):
                        value = "ssd"
                    else:
                        value = "hdd"
                elif any(x in value for x in ["ssd", "pcie", "pci", "m.2", "nvme"]):
                    value = "ssd"
                elif "hdd" in value:
                    value = "hdd"
                elif "emmc" in value:
                    value = "emmc"
                
                self.adapter['storage_type'] = value
            except Exception as e:
                print("Error in storage type transformation:", e)
                print("Error at:", self.adapter.get('name'))
            
        def transform_webcam_resolution(self):
            """Transforms the webcam resolution field to a standardized format."""
            try:
                # Get the webcam resolution field value
                value = self.adapter.get('webcam_resolution')
                if value == "n/a":
                    value = "no"
                else:
                    value = "yes"
                self.adapter['webcam_resolution'] = value
            except Exception as e:
                print("Error in webcam resolution transformation:", e)
                print("Error at:", self.adapter.get('name'))
            
        def transform_screen_size(self):
            """Transforms the screen size field to a standardized format."""
            try:
                # Get the screen size field value
                value = self.adapter.get('screen_size')
                if value == "n/a":
                    return
                
                value = value.replace(',', '.')
                
                value = re.search(r'(\d+(\.\d+)?)\s*(["\']|(-)?\s*inch|”)', value)
                
                if value:
                    value = float(value.group(1))
                else:
                    value = "n/a"
                self.adapter['screen_size'] = value
            except Exception as e:
                print("Error in screen size transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_screen_resolution(self):
            """Transforms the screen resolution field to a standardized format."""
            try:
                # Get the screen resolution field value
                value = self.adapter.get('screen_resolution')
                if value == "n/a":
                    return
                
                value = ''.join(value.split())
                value = value.replace('*', 'x')
                
                search_value = re.search(r'(\d{3,4})\s*x\s*(\d{3,4})', value)
                if search_value:
                    width, height = sorted(map(int, search_value.groups()), reverse=True)
                    value = f"{width}x{height}"
                else:
                    resolution_widths = {
                        'fhd': 1920,       # Full HD
                        '2k': 2048,        # 2K (Cinemascope)
                        'qhd': 2560,       # Quad HD (1440p)
                        '2.5k': 2560,      # 2.5K Resolution
                        '3k': 3072,        # 3K (Example)
                        '4k': 3840,        # Ultra HD 4K
                        '5k': 5120,        # 5K Resolution
                        '8k': 7680,        # 8K Ultra HD
                        'fullhd+': 1920,   # Full HD+ with 16:10 ratio
                        'wuxga': 1920,     # WUXGA with 16:10 ratio
                    }

                    ratio_match = re.search(r'(\d+):(\d+)', value)

                    for resolution, width in resolution_widths.items():
                        if resolution in value:
                            if ratio_match:
                                width_ratio = int(ratio_match.group(1))
                                height_ratio = int(ratio_match.group(2))
                            else:
                                if resolution in ['fullhd+', 'wuxga']:
                                    width_ratio, height_ratio = 16, 10  # 16:10 aspect ratio
                                else:
                                    width_ratio, height_ratio = 16, 9   # Default to 16:9

                            height = (width * height_ratio) // width_ratio
                            
                            value = f"{width}x{height}"
                            break  # Exit loop after finding the first matching resolution

                
                self.adapter['screen_resolution'] = value
            except Exception as e:
                print("Error in screen resolution transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_screen_refresh_rate(self):
            """Transforms the screen refresh rate field to a standardized format."""
            try:
                # Get the screen refresh rate field value
                value = self.adapter.get('screen_refresh_rate')
                if value == "n/a":
                    return
                
                invalid_vals = ["đang cập nhật", "hãng không công bố"]
                if any(invalid_val in value for invalid_val in invalid_vals):
                    value = "n/a"
                
                search_value = re.search(r'\d+\s*hz', value)
                if search_value:
                    value = search_value.group()
                    value = int(value.split('hz')[0])
                else: 
                    value = "n/a"
                
                self.adapter['screen_refresh_rate'] = value
            except Exception as e:
                print("Error in screen refresh rate transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_screen_brightness(self):
            """Transforms the screen brightness field to a standardized format."""
            try:
                # Get the screen brightness field value
                value = self.adapter.get('screen_brightness')
                if value == "n/a":
                    return
                
                search_value = re.search(r'\d+\s*nits', value)
                if search_value:
                    value = search_value.group()
                    value = int(value.split('nits')[0])
                
                else: 
                    value = "n/a"
                
                self.adapter['screen_brightness'] = value
            except Exception as e:
                print("Error in screen brightness transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_battery_capacity(self):
            """Transforms the battery capacity field to a standardized format."""
            try:
                # Get the battery capacity field value
                value = self.adapter.get('battery_capacity')
                if value == "n/a":
                    return
                
                value = value.replace(',', '.')
                value = re.sub(r'[():]|nguồn', '', value).strip()

                search_value = re.search(r'(\d+(?:\.\d+)?)\s*(w|wh|battery)', value)
                if search_value:
                    value = float(search_value.group(1))
                
                self.adapter['battery_capacity'] = value
            except Exception as e:
                print("Error in battery capacity transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_battery_cells(self):
            """Transforms the number of battery cells field to a standardized format."""
            try:
                # Get the number of battery cells field value
                value = self.adapter.get('battery_cells')
                if value == "n/a":
                    return
                
                search_value = re.search(r'(\d+)[ -]?cell(?:s)?|(\d+)\s+cells|chân\s*(\d+)', value)
                
                if search_value:
                    value = int(next(g for g in search_value.groups() if g is not None))
                elif "integrated" in value:
                    value = "n/a"
                
                self.adapter['battery_cells'] = value
            except Exception as e:
                print("Error in battery cells transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_size(self):
            """Transforms the size field to a standardized format."""
            def na_exit():
                self.adapter['width'] = "n/a"
                self.adapter['depth'] = "n/a"
                self.adapter['height'] = "n/a"
                
                del self.adapter['size']
            
            try:
                value = self.adapter.get('size')
                if value == "n/a":
                    na_exit()
                    return
                
                value = value.replace(',', '.')

                numbers = re.findall(r'\d+\.?\d*', value)
                if len(numbers) < 3:
                    na_exit()
                    return
                
                extracted_numbers = numbers[:3]
                hyphenated_number = re.search(r'-(\d+\.?\d*)', value)
                if hyphenated_number:
                    extracted_numbers[-1] = hyphenated_number.group(1)
                
                extracted_numbers = [float(num) for num in extracted_numbers]
                extracted_numbers = sorted(extracted_numbers, reverse=True)
                
                self.adapter['width'] = round(extracted_numbers[0] if extracted_numbers[0] < 100 else extracted_numbers[0] / 10, 2)
                self.adapter['depth'] = round(extracted_numbers[1] if extracted_numbers[1] < 100 else extracted_numbers[1] / 10, 2)
                self.adapter['height'] = round(extracted_numbers[2] if extracted_numbers[2] < 3  else extracted_numbers[2] / 10, 2)
                
                del self.adapter['size']
            except Exception as e:
                print("Error in size transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_weight(self):
            """Transforms the weight field to a standardized format."""
            try:
                value = self.adapter.get('weight')
                if value == "n/a":
                    return
            
                value = value.replace(',', '.')
            
                value_kg = re.search(r'(\d+(\.\d+)?)\s*(kg)', value)
                value_g = re.search(r'(\d+(\.\d+)?)\s*(gram|g)', value)
                
                if value_kg:
                    value = float(value_kg.group(1))
                elif value_g:
                    value = float(value_g.group(1)) / 1000
                    
                self.adapter['weight'] = value
            except Exception as e:
                print("Error in weight transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        
        def transform_connectivity(self):
            """Transforms the connectivity field to a standardized format."""
            try:
                value = self.adapter.get('connectivity')
                if value == "n/a":
                    self.adapter['number_usb_a_ports'] = "n/a"
                    self.adapter['number_usb_c_ports'] = "n/a"
                    self.adapter['number_hdmi_ports'] = "n/a"
                    self.adapter['number_ethernet_ports'] = "n/a"
                    self.adapter['number_audio_jacks'] = "n/a"
                    
                    del self.adapter['connectivity']
                    return
            
                def count_number_usb(value, get_a=True):
                    # pattern_a = r'\b(type[- ]?a|standard[- ]?a|usb[- ]?a|usb[- ]?3\.2|usb[- ]?3\.0)\b'
                    # pattern_c = r'\b(type[- ]?c|standard[- ]?c|thunderbolt|usb[- ]?c)\b'
                    
                    pattern_a = r'\b(\d+)\s*x\s*(type[- ]?a|standard[- ]?a|usb[- ]?a|usb[- ]?3\.2|usb[- ]?3\.0)\b'
                    pattern_c = r'\b(\d+)\s*x\s*(type[- ]?c|standard[- ]?c|thunderbolt|usb[- ]?c)\b'
                    
                    if re.sub(r'^\s*[•-].*\n?', '', value, flags=re.MULTILINE) != '':
                        value = re.sub(r'^\s*[•-].*\n?', '', value, flags=re.MULTILINE)
                    
                    while '(' in value and ')' in value:
                        value = re.sub(r'\([^()]*\)', '', value)
                    
                    value = re.split(r'[\n,]', value)
                    count = 0
                    for line in value:
                        if get_a:
                            if re.search(pattern_a, line) and not re.search(pattern_c, line):
                                line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
                                val = line.split()[0]
                                if val[-1] == 'x': val = val[:-1]
                        
                                if val.isnumeric():
                                    count += int(val)
                                else:
                                    count += 1
                        else:
                            if re.search(pattern_c, line):
                                line = re.sub(r'^[^a-zA-Z0-9]+', '', line)
                                val = line.split()[0]
                                if val[-1] == 'x': val = val[:-1]
                        
                                if val.isnumeric():
                                    count += int(val)
                                else:
                                    count += 1
                    
                    return count
                    
                self.adapter['number_usb_a_ports'] = count_number_usb(value, get_a=True)
                self.adapter['number_usb_c_ports'] = count_number_usb(value, get_a=False)
                
                def has_port(value, pattern):
                    if value:
                        port_search = re.search(pattern, value)
                        return 1 if port_search else 0
                    else:
                        return "n/a"
                
                self.adapter['number_hdmi_ports'] = has_port(value, r'\b(hdmi)\b')
                self.adapter['number_ethernet_ports'] = has_port(value,  r'\brj-45|ethernet\b')
                self.adapter['number_audio_jacks'] = has_port(value, r'\bheadphone|3.5mm\b')
            
                del self.adapter['connectivity']
            except Exception as e:
                print("Error in connectivity transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_default_os(self):
            """Transforms the default OS field to a standardized format."""
            try:
                value = self.adapter.get('default_os')
                if value == "n/a":
                    return
                
                if self.adapter.get('brand') == 'apple':
                    value = 'macos'
                elif "no" in value:
                    value = "n/a"
                elif "chrome" in value:
                    value = "chrome os"
                elif any(_ in value for _ in ["ubuntu", "linux", "free"]):
                    value = "linux"
                else:
                    for removal in ['single language', 'sl', '64', 'bit', 'sea', 'microsoft', 'office']:
                        value = value.replace(removal, '')
                    value = ' '.join(value.split())
                    
                    if 'win' in value and 'windows' not in value:
                        value = value.replace('win', 'windows')
                    
                    search_value = re.search(r"windows\s+\d{1,2}(\.\d+)?(\s+\w+)?(\s+\w+)?", value)
                    
                    if search_value:
                        value = search_value.group()
                        
                    value = re.sub(r'[^\x20-\x7E]', '', value)
                    for end in ['home', 'pro', 'enterprise', 'education', 's', 'ltsc', 'ltsc', 'n']:
                        if end in value:
                            value = value[:value.index(end) + len(end)]
                            break
                    if 'windows' in value:
                        value = value[value.index('windows'):]
                
                self.adapter['default_os'] = value
            except Exception as e:
                print("Error in default OS transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_warranty(self):
            """Transforms the warranty field to a standardized format."""
            try:
                value = self.adapter.get('warranty')
                if type(value) == list:
                    value = " ".join([i.replace('\n', '').strip() for i in value])
                    
                if value == "n/a":
                    return
                
                match = re.search(r'(\d+)\s*(tháng|năm|years?)', value)
                if match:
                    number = int(match.group(1))
                    unit = match.group(2)
                    if unit == 'tháng':
                        value = number
                    else:  # 'năm' or 'year(s)'
                        value = number * 12
                else:
                    value = "aaaaaaaaaaa"
                
                self.adapter['warranty'] = value
            except Exception as e:
                print("Error in warranty transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_price(self):
            """Transforms the price field to a standardized format."""
            try:
                value = self.adapter.get('price')
                if value == "n/a":
                    return
                
                value = value.replace('.', '')
                value = value.replace('*', '')
                value = re.sub(r'[đ₫]', '', value).strip()
                
                self.adapter['price'] = value
            except Exception as e:
                print("Error in price transformation:", e)
                print("Error at:", self.adapter.get('name'))
                
        def transform_all(self):
            """Transforms all fields."""
            self.transform_cpu()
            self.transform_vga()
            self.transform_ram_amount()
            self.transform_ram_type()
            self.transform_storage_amount()
            self.transform_storage_type()
            self.transform_webcam_resolution()
            self.transform_screen_size()
            self.transform_screen_resolution()
            self.transform_screen_refresh_rate()
            self.transform_screen_brightness()
            self.transform_battery_capacity()
            self.transform_battery_cells()
            self.transform_size()
            self.transform_weight()
            self.transform_connectivity()
            self.transform_default_os()
            self.transform_warranty()
            self.transform_price()
            
            if self.debug_mode:
                pprint.pprint(self.adapter.asdict(), indent=4) 