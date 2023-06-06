from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from weather_v01 import weather_now

default_args = {
    "owner": "fox",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)

}

with DAG(
        default_args=default_args,
        dag_id="weather",
        description="weather DAG",
        start_date=datetime(2023, 5, 21),
        schedule="1 * * * *"
) as dag:
    scraping_weather = PythonOperator(
        task_id="scraping_weather",
        python_callable=weather_now
    )

    create_table_weather = PostgresOperator(
        task_id="create_table_weather",
        postgres_conn_id="postgres_localhost",
        sql="""
                CREATE TABLE IF NOT EXISTS weather_data (
                    date VARCHAR(200),
                    current_temperature VARCHAR(200),
                    feels_like VARCHAR(200),
                    sky VARCHAR(200),
                    chance_of_precipitation VARCHAR(200),
                    wind VARCHAR(200), 
                    pressure VARCHAR(200), 
                    uv_index VARCHAR(200), 
                    humidity VARCHAR(200), 
                    precipitation VARCHAR(200),
                    timestamps VARCHAR(200)
            )
            """

    )

    add_data_in_weather = PostgresOperator(
        task_id="add_data_in_weather",
        postgres_conn_id="postgres_localhost",
        sql="""
            insert into weather_data (date, current_temperature, feels_like, sky, chance_of_precipitation, wind, 
            pressure, uv_index, humidity, precipitation, timestamps) values 
            ('{{ti.xcom_pull(task_ids='scraping_weather')['time']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['current_temperature']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['feels_like']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['sky']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['chance_of_precipitation']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['wind']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['pressure']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['uv_index']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['humidity']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['precipitation']}}',
            '{{ti.xcom_pull(task_ids='scraping_weather')['timestamps']}}'
            )
            """
    )
scraping_weather >> create_table_weather >> add_data_in_weather
