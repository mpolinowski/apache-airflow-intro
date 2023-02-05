from airflow import DAG
from airflow.decorators import task

from datetime import datetime

from include.datasets import DATASET_01


start_date = datetime(2023,2,5)
description = "Data pre-processing"
tags = ['scheduler', 'producer']
dag_id = 'producer'
schedule = '@daily'

with DAG(
    dag_id=dag_id,
    start_date=start_date,
    schedule=schedule,
    catchup=False,
    description=description,
    tags=tags
    ):

    ## decorator with outlet so updates
    ## to dataset can be used as trigger
    @task(outlets=[DATASET_01])
    ## preprocess data and write to file
    def preprocess_dataset():
        with open(DATASET_01.uri, 'a+') as file:
            file.write('preprocessed data ready for consumption')

    preprocess_dataset()