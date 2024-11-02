from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import timezone, timedelta, days_ago
from airflow.utils.task_group import TaskGroup

from sql_helper import *

# [DEFINE DAG]
default_args = {
    'owner': 'veil',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

main_dag = DAG(
    'main_dag',
    default_args=default_args,
    description='The DAG control all the tasks for the project',
    schedule_interval='@monthly',
    start_date=days_ago(1),
    max_active_tasks=2,
)

# [SCRAPING TASK]
laptopshop_names = ['gearvn', 'cellphones']
with TaskGroup('laptop_scraping_tasks', dag=main_dag) as laptop_scraping_tasks:
    for name in laptopshop_names:
        task = BashOperator(
            task_id=f'scrape_{name}',
            bash_command='cd /app/scraper && scrapy crawl {}_spider -O ../temp/{}_data.json'.format(name, name),
            pool='default_pool',
            do_xcom_push=False,
            dag=main_dag,
        )

# [POSTGRES TASK]
# Create laptop specs table
create_laptop_specs_table_task = PostgresOperator(
    task_id='create_laptop_specs_table',
    postgres_conn_id='postgres_default',
    sql=get_create_laptop_specs_table_sql(timezone.utcnow().month, timezone.utcnow().year),
    pool='default_pool',
    dag=main_dag,
)

# Insert data into laptop specs table
insert_into_laptop_specs_table_sql = PostgresOperator(
    task_id='insert_into_laptop_specs_table',
    postgres_conn_id='postgres_default',
    sql=get_insert_into_laptop_specs_table_sql(['/app/temp/{}_data.json'.format(name) for name in laptopshop_names], 
                                               timezone.utcnow().month, 
                                               timezone.utcnow().year),
    pool='default_pool',
    dag=main_dag,
)

# [DEFINE DIRECTED ACYCLIC GRAPH]
# laptop_scraping_tasks >> 
laptop_scraping_tasks >> create_laptop_specs_table_task >> insert_into_laptop_specs_table_sql