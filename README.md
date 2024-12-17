# laptop-price-prediction-ds-prj
This project aims to develop a data analysis cycle focused on predicting laptop prices. All content in this project is created for the IT4142E module at Hanoi University of Science and Technology.

# How to run the project
This project is built to be run on Docker containers. To run the project, you need to have Docker installed on your device. If you don't have Docker installed, please follow the instructions on the [official Docker website](https://docs.docker.com/get-docker/).

To run the project, follow these steps:
1. Clone the project to your local machine by running the following command in your terminal:
```bash
git clone https://github.com/auphong2707/laptop-price-prediction-ds-prj.git

cd laptop-price-prediction-ds-prj
```

2. Ensure that the **End of Line Sequence** of the `entrypoint.sh` file is set to **LF**.

3. Build the Docker image by running the following command:
```bash
docker build -t laptop-price-prediction-image .
```

4. Run the Docker container by running the following command:
```bash
docker run -d -p 5000:5000 -p 8080:8080 laptop-price-prediction-image
```
(The port **5000** is used for the Flask Web Application, and the port **8080** is used for the Airflow web server.)

From now on, you can access the Flask Web Application at `http://localhost:5000` and the Airflow web server at `http://localhost:8080`.

There are 3 pages in the web application:

- **Predictor page**: This page is used to predict the price of a laptop based on the laptop's specifications.
- **Data analysis page**: This page shows the data analysis results. The results can be downloaded as a PDF file.
- **Database page**: This page shows the data in the database. The data can be downloaded as a CSV file.

## Important notice
In the first run, there would be no data in the database, hence the 
Flask Web Application would notify an error: **An error occurred: 'NoneType' object is not subscriptable. It could be that there is no data in the database.**. Therefore, you need to run the `main_dag` in Airflow to start the first cycle of dataflow to get the data and model. To do this, follow these steps:

1. Access the Airflow web server at `http://localhost:8080`.
2. Login with username `admin` and password `admin`.
3. Click on `main_dag`, then click the `Trigger DAG` button *(The triangle button in the right corner of the screen)*.
   
   **Note:** This process would take a few hours to complete. You can check the status of the process by clicking on `main_dag` and then clicking the `Graph View` button.

After the process is completed, you can access our web application at `http://localhost:5000`.

# Project source code checking
If you want to check the source code of the project for examination purposes, we prepared:
- **Scraped data**: 
  - The scraped data is stored in the `./data_analysis/data` folder. It is stored in CSV files, separated by the month_year it was scraped.
  - You can check the raw data in the `./temp` folder.
- **Analysis**: 
  - The analysis jupyter notebook `EDA.ipynb` is stored in the `./data_analysis` folder. This contains all of the data analysis code **without the conclusion**. The EDA with conclusion is made manually and **is not stored** in the repository.
  - The analysed EDA is saved in HTML format in the `./data_analysis/results/eda` folder.
- **Trained models**:
  - The models are stored in `./data_analysis/results/trained_models` folder. They are stored in `.joblib` files, separated by the month_year they were trained.
- **Training, Preprocess and Predicting code**: 
  - The training, preprocess and predicting code are stored in the `./data_analysis` folder. They are stored in the `train.py`, `preprocess.py` and `predict.py` files.
- **Database SQL code**:
  - The database SQL code is generated in `./airflow/dags/database/sql_helper.py` file. This file is used by Airflow to insert data into the database.
- **Scraper code**:
  - The code for scraper is stored in the `./scraper` folder.
  - Our **spiders** are stored in the `./scraper/scraper/spiders` folder.
    - `base_laptopshop_spider.py` contains the base spider classes that are used to be inherited by other spiders.
    - Remaining spiders are the spiders used to scrape data from the websites. *(2 deprecated ones are those where websites cannot be scraped)*
  - Our **transformation pipelines** is stored in the `./scraper/scraper/pipelines` folder.

I hope you enjoy checking our source code. If you have any questions, feel free to ask us.
