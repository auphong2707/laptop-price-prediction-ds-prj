from flask import Flask, render_template, request, redirect, url_for

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

@app.route('/database')
def database():
    sample_data = [
        {"id": 1, "name": "Item A", "value": 100},
        {"id": 2, "name": "Item B", "value": 200},
        {"id": 3, "name": "Item C", "value": 300}
    ]
    return render_template('database.html', data=sample_data)


if __name__ == '__main__':
    app.run(debug=True)
