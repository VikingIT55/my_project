from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from refresh_token import Refresh
from Spotify_ETL import run_spotify_etl
from weather_v01 import weather_now
fresh_token = Refresh()

default_args = {
    "owner": "fox",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)

}

with DAG(
        default_args=default_args,
        dag_id="ETL",
        description="spotify_ETL",
        start_date=datetime(2023, 5, 21),
        schedule="0 17 * * *"
) as dag:
    refresh_token = PythonOperator(
        task_id="refresh_token",
        python_callable=fresh_token.refresh
    )

    ETL = PythonOperator(
        task_id="ETL",
        python_callable=run_spotify_etl

    )
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            CREATE TABLE IF NOT EXISTS spotify_data (
                played_at VARCHAR(200),
                artist VARCHAR(200),
                name_track VARCHAR(200),
                timestamps VARCHAR(200),
                CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
        """

    )
    add_data_in_database = PostgresOperator(
        task_id="add_data_in_database",
        postgres_conn_id="postgres_localhost",
        sql="""
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][0]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][0]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][0]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][0]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][1]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][1]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][1]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][1]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][2]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][2]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][2]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][2]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][3]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][3]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][3]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][3]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][4]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][4]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][4]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][4]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][5]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][5]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][5]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][5]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][6]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][6]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][6]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][6]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][7]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][7]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][7]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][7]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][8]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][8]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][8]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][8]}}'
            );
            insert into spotify_data (played_at, artist, name_track, timestamps) values 
            ('{{ti.xcom_pull(task_ids='ETL')['played_at'][9]}}',
            '{{ti.xcom_pull(task_ids='ETL')['artist'][9]}}',
            '{{ti.xcom_pull(task_ids='ETL')['name_track'][9]}}',
            '{{ti.xcom_pull(task_ids='ETL')['timestamps'][9]}}'
            )
            """
    )
'''    scraping_weather = PythonOperator(
        task_id="scraping weather",
        python_callable=weather_now()
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
                    CONSTRAINT primary_key_constraint PRIMARY KEY (date)
            )
            """

    )

    add_data_in_weather = PostgresOperator(
        task_id="add_data_in_weather",
        postgres_conn_id="postgres_localhost",
        sql="""
            insert into weather_data (date, current_temperature, feels_like, sky, chance_of_precipitation, wind, pressure, 
            uv_index, humidity, precipitation) values 
            ('{{ti.xcom_pull(task_ids='scraping weather')[0]}}',
            '{{ti.xcom_pull(task_ids='scraping weather')[1]}}',
            '{{ti.xcom_pull(task_ids='scraping weather')[2]}}',
            '{{ti.xcom_pull(task_ids='scraping weather')[3]}}'
            )
            """
    )'''

refresh_token >> ETL >> create_table >> add_data_in_database
#scraping_weather >> create_table_weather >> add_data_in_weather