from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_arg = {
    'owner': 'airflow',
    'depens_on_past': False,
    'start_date': datetime(2023, 1, 9),
    'email': ['foxkarasava55@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'spotify_dag',
    default_arg=default_arg,
    description='DAG with ETL process',
    schedule_interval=timedelta(days=1)
)

run_etl = PythonOperator(
    task_id='whole_spotify_etl',
    dag=dag
)
run_etl
