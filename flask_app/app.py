import io
import os
from flask import Flask, render_template, request, redirect, send_file, send_from_directory, url_for
import pdfkit

import sys
sys.path.append('.')
from helper import *
from data_analysis.predict import predict

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('predictor'))

@app.route('/predictor', methods=['GET', 'POST'])
def predictor():
    try:
        BRAND_LIST = ['lenovo', 'hp', 'asus', 'acer', 'dell', 'apple', 'msi', 'lg', 'gigabyte', 'microsoft']
        CPU_LIST = sorted(get_latest_table('cpu_specs')['name'].tolist())
        GPU_LIST = sorted(get_latest_table('gpu_specs')['name'].tolist())
        SCREEN_RESOLUTION_LIST = sorted(get_latest_table('laptop_specs')['screen_resolution'].dropna().unique().tolist())

        if request.method == 'POST':
            # Collect all form data
            form_data = dict(request.form)
            
            for key, value in form_data.items():
                if form_data[key] == 'NONE':
                    form_data[key] = None
            
            for key in ['storage_type', 'ram_type']:
                if form_data[key] is not None:
                    form_data[key] = form_data[key].lower()
            
            for key in ['ram_amount', 'storage_amount', 'screen_refresh_rate', 'screen_brightness', 'battery_cells',
                        'number_usb_a_ports', 'number_usb_c_ports', 'number_hdmi_ports', 'number_ethernet_ports', 'number_audio_jacks',
                        'warranty']:
                if form_data[key] is not None:
                    form_data[key] = int(form_data[key])
            
            for key in ['screen_size', 'battery_capacity', 'weight', 'width', 'depth', 'height']:
                if form_data[key] is not None:
                    form_data[key] = float(form_data[key])
            
            # For demonstration, just echo the input
            prediction = f"Our price prediction for your laptop specification is: {int(round(predict(form_data), -3)):,} VNĐ".replace(",", ".")
            
            return render_template('predictor.html', 
                                brands=BRAND_LIST, 
                                cpus=CPU_LIST, 
                                gpus=GPU_LIST,
                                screen_resolutions=SCREEN_RESOLUTION_LIST,
                                prediction=prediction)

        return render_template('predictor.html', 
                            brands=BRAND_LIST, 
                            cpus=CPU_LIST, 
                            gpus=GPU_LIST,
                            screen_resolutions=SCREEN_RESOLUTION_LIST)
    except Exception as e:
        return "An error occurred: " + str(e) + ". It could be that there is no data in the database."

EDA_PATH = '/app/data_analysis/results/eda/'

@app.route('/data_analysis/<eda_name>')
def data_analysis(eda_name):
    try:
        EDA_LIST = [f for f in os.listdir(EDA_PATH) if os.path.isfile(os.path.join(EDA_PATH, f))]
        
        if eda_name == 'default_eda':
            # Redirect to the first EDA file if none is specified
            return redirect(url_for('data_analysis', eda_name=EDA_LIST[0]))
        
        # Pass the list of files and the active file to the template
        return render_template(
            "data_analysis.html", 
            eda_list=EDA_LIST, 
            active_eda=eda_name
        )
    except Exception as e:
        return "An error occurred: " + str(e) + ". It could be that there is no data in the database."
    
@app.route('/download_pdf/<eda_name>')
def download_pdf(eda_name):
    file_path = os.path.join(EDA_PATH, eda_name)
    
    if os.path.isfile(file_path):
        # Define PDF options to adjust width
        options = {
            'page-width': '300mm',
            'page-height': '297mm',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm'
        }
        
        # Convert HTML file to PDF with the above options
        pdf_output = pdfkit.from_file(file_path, False, options=options)
        
        # Return the PDF as a response
        return send_file(
            io.BytesIO(pdf_output), 
            mimetype='application/pdf', 
            as_attachment=True, 
            download_name=f"{eda_name.replace('.html', '.pdf')}"
        )
    else:
        return f"File {eda_name} not found", 404

@app.route('/serve_eda/<eda_name>')
def serve_eda(eda_name):
    # Serve the selected EDA file for iframe rendering
    if os.path.isfile(os.path.join(EDA_PATH, eda_name)):
        print(EDA_PATH, eda_name)
        return send_from_directory(EDA_PATH, eda_name)
    else:    
        return f"File {eda_name} not found", 404

@app.route('/database/<table_name>')
def database(table_name):
    try:
        TABLE_LIST = get_table_list()
        
        if table_name == 'default_table':
            return redirect(url_for('database', table_name=TABLE_LIST[0]))
        
        df = get_table(table_name)
        
        # Convert DataFrame to HTML
        table_html = df.to_html(classes='dataframe', index=False, border=0)
        
        return render_template('database.html', 
                            table_name=table_name, 
                            table_list=TABLE_LIST, 
                            table_html=table_html,
                            active_table=table_name
                            )
    except Exception as e:
        return "An error occurred: " + str(e) + ". It could be that there is no data in the database."
    
@app.route('/download_csv/<table_name>')
def download_csv(table_name):
    df = get_table(table_name)
    
    # Convert the DataFrame to a CSV in memory
    csv = df.to_csv(index=False)
    
    # Create an in-memory binary stream to serve as the file
    response = io.BytesIO()
    response.write(csv.encode())
    response.seek(0)
    
    # Send the file to the user
    return send_file(response, mimetype='text/csv', as_attachment=True, download_name=f'{table_name}.csv')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
