import gc
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import timezone, timedelta, days_ago
from airflow.utils.task_group import TaskGroup

# Define default arguments
default_args = {
    'owner': 'veil',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'main_dag',
    default_args=default_args,
    description='The DAG control all the tasks for the project',
    schedule_interval='@monthly',
    start_date=days_ago(1),
    max_active_tasks=2,
) as main_dag:
    # [SCRAPING TASK]
    laptopshop_names = ['gearvn', 'cellphones']

    with TaskGroup('laptop_scraping_tasks') as laptop_scraping_tasks:
        for name in laptopshop_names:
            task = BashOperator(
                task_id=f'scrape_{name}',
                bash_command='cd /app/scraper && scrapy crawl {}_spider -O ../temp/{}_data.json'.format(name, name),
                pool='default_pool',
                do_xcom_push=False
            )

    # [INTEGRATION TASK]
    integration_task = BashOperator(
        task_id='integration',
        bash_command='echo "Integration task"',
    )

    # [DEFINE DIRECTED ACYCLIC GRAPH]
    laptop_scraping_tasks >> integration_task