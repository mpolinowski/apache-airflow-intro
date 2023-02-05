from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

from include.datasets import DATASET_01

start_date = datetime(2023,2,5)
description = "Start this pipeline when new data arrives"
tags = ['scheduler', 'consumer']
dag_id = 'consumer'

with DAG(
    start_date=start_date,
    dag_id=dag_id,
    schedule=[DATASET_01],
    catchup=False,
    description=description,
    tags=tags
    ):

    @task
    ## process prepared data and write to file
    def process_dataset():
        with open(DATASET_01.uri, 'r') as file:
            print(file.read())

    process_dataset()