from airflow import DAG 
from airflow.decorators import task

from datetime import datetime

start_date = datetime(2023,2,6)
tags=['generated']

with DAG(
    dag_id = 'get_price_FB',
    start_date = start_date,
    schedule = '@weekly',
    catchup = False,
    tags = tags
    ):

    @task
    def extract(symbol):
        return symbol

    @task
    def process(symbol):
        return symbol

    @task
    def store(symbol):
        return symbol

    store(process(extract(123)))
