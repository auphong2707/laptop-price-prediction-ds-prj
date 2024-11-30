import io
from flask import Flask, render_template, request, redirect, send_file, url_for
import pandas as pd
from helper import *

TABLE_LIST = get_table_list()

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('predictor'))

@app.route('/predictor', methods=['GET', 'POST'])
def predictor():
    if request.method == 'POST':
        # Collect all form data
        form_data = request.form
        # For demonstration, just echo the input
        prediction = f"Received input: {form_data}"
        return render_template('predictor.html', prediction=prediction)
    return render_template('predictor.html')

@app.route('/data_analysis')
def data_analysis():
    analysis_results = {"mean": 50, "median": 45, "std_dev": 5}  # Dummy data
    return render_template('data_analysis.html', results=analysis_results)

@app.route('/database/<table_name>')
def database(table_name):
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
    app.run(debug=True)
