from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import timezone, timedelta, days_ago
from airflow.utils.task_group import TaskGroup

from database.integrity_check import check_integrity_all
from database.sql_helper import *


default_args = {
    'owner': 'veil',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

test_dag = DAG(
    'test_dag',
    default_args=default_args,
    description='Test DAG before running the main DAG',
    schedule_interval='@monthly',
    start_date=days_ago(1),
    max_active_tasks=2,
)

# with TaskGroup('specifications_scraping_tasks', dag=test_dag) as specifications_scraping_tasks:
#     cpu_scrape_task = BashOperator(
#         task_id='cpu_scrape_task',
#         bash_command='cd /app/scraper && scrapy crawl cpu_spider -O ../temp/cpu_data.json',
#         pool='default_pool',
#         do_xcom_push=False,
#         dag=test_dag,
#     )

#     gpu_scrape_task = BashOperator(
#         task_id='gpu_scrape_task',
#         bash_command='cd /app/scraper && scrapy crawl gpu_spider -O ../temp/gpu_data.json',
#         pool='default_pool',
#         do_xcom_push=False,
#         dag=test_dag,
#     )

laptopshop_names = ['gearvn', 'cellphones']

# [POSTGRES TASK]
with TaskGroup('database_tasks', dag=test_dag) as database_tasks:
    # SQL generation tasks
    create_cpu_specs_table_sql = PythonOperator(
        task_id='create_cpu_specs_table_sql',
        python_callable=get_create_cpu_specs_table_sql,
        op_args=[timezone.utcnow().month, timezone.utcnow().year],
        dag=test_dag
    )
    
    insert_into_cpu_specs_table_sql = PythonOperator(
        task_id='insert_into_cpu_specs_table_sql',
        python_callable=get_insert_into_cpu_specs_table_sql,
        op_args=['./temp/cpu_data.json', timezone.utcnow().month, timezone.utcnow().year],
        dag=test_dag,
    )
    
    create_gpu_specs_table_sql = PythonOperator(
        task_id='create_gpu_specs_table_sql',
        python_callable=get_create_gpu_specs_table_sql,
        op_args=[timezone.utcnow().month, timezone.utcnow().year],
        dag=test_dag,
    )
    
    insert_into_gpu_specs_table_sql = PythonOperator(
        task_id='insert_into_gpu_specs_table_sql',
        python_callable=get_insert_into_gpu_specs_table_sql,
        op_args=['./temp/gpu_data.json', timezone.utcnow().month, timezone.utcnow().year],
        dag=test_dag,
    )
    
    create_laptop_specs_table_sql = PythonOperator(
        task_id='create_laptop_specs_table_sql',
        python_callable=get_create_laptop_specs_table_sql,
        op_args=[timezone.utcnow().month, timezone.utcnow().year],
        dag=test_dag,
    )
    
    insert_into_laptop_specs_table_sql = PythonOperator(
        task_id='insert_into_laptop_specs_table_sql',
        python_callable=get_insert_into_laptop_specs_table_sql,
        op_args=[['./temp/{}_data.json'.format(name) for name in laptopshop_names], timezone.utcnow().month, timezone.utcnow().year],
        dag=test_dag,
    )
    
    # CPU specs table
    create_cpu_specs_table_task = PostgresOperator(
        task_id='create_cpu_specs_table_task',
        postgres_conn_id='postgres_default',
        sql="{{ task_instance.xcom_pull(task_ids='database_tasks.create_cpu_specs_table_sql') }}",
        pool='default_pool',
        dag=test_dag,
        
    )

    insert_into_cpu_specs_table_task = PostgresOperator(
        task_id='insert_into_cpu_specs_table_task',
        postgres_conn_id='postgres_default',
        sql="{{ task_instance.xcom_pull(task_ids='database_tasks.insert_into_cpu_specs_table_sql') }}",
        pool='default_pool',
        dag=test_dag,
        
    )

    # GPU specs table
    create_gpu_specs_table_task = PostgresOperator(
        task_id='create_gpu_specs_table_task',
        postgres_conn_id='postgres_default',
        sql="{{ task_instance.xcom_pull(task_ids='database_tasks.create_gpu_specs_table_sql') }}",
        pool='default_pool',
        dag=test_dag,
        
    )

    insert_into_gpu_specs_table_task = PostgresOperator(
        task_id='insert_into_gpu_specs_table_task',
        postgres_conn_id='postgres_default',
        sql="{{ task_instance.xcom_pull(task_ids='database_tasks.insert_into_gpu_specs_table_sql') }}",
        pool='default_pool',
        dag=test_dag,
        
    )

    # Laptop specifications table
    create_laptop_specs_table_task = PostgresOperator(
        task_id='create_laptop_specs_table_task',
        postgres_conn_id='postgres_default',
        sql="{{ task_instance.xcom_pull(task_ids='database_tasks.create_laptop_specs_table_sql') }}",
        pool='default_pool',
        dag=test_dag,
        
    )

    insert_into_laptop_specs_table_task = PostgresOperator(
        task_id='insert_into_laptop_specs_table_task',
        postgres_conn_id='postgres_default',
        sql="{{ task_instance.xcom_pull(task_ids='database_tasks.insert_into_laptop_specs_table_sql') }}",
        pool='default_pool',
        dag=test_dag,
        
    )
    
    check_integrity_task = PythonOperator(
        task_id='check_integrity',
        python_callable=check_integrity_all,
        dag=test_dag,
        
    )

# [DEFINE DIRECTED ACYCLIC GRAPH]
# cpu_scrape_task >> [create_cpu_specs_table_sql, insert_into_cpu_specs_table_sql]
# gpu_scrape_task >> [create_gpu_specs_table_sql, insert_into_gpu_specs_table_sql]

[create_cpu_specs_table_sql, insert_into_cpu_specs_table_sql] >> create_cpu_specs_table_task >> insert_into_cpu_specs_table_task
[create_gpu_specs_table_sql, insert_into_gpu_specs_table_sql] >> create_gpu_specs_table_task >> insert_into_gpu_specs_table_task

create_laptop_specs_table_sql >> create_laptop_specs_table_task
insert_into_laptop_specs_table_sql >> insert_into_laptop_specs_table_task
create_laptop_specs_table_task >> insert_into_laptop_specs_table_task

insert_into_laptop_specs_table_task >> check_integrity_task

[create_cpu_specs_table_task, create_gpu_specs_table_task] >> create_laptop_specs_table_task
[insert_into_cpu_specs_table_task, insert_into_gpu_specs_table_task] >> insert_into_laptop_specs_table_task