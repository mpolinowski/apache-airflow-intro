from airflow.models import DAG
from airflow.sensors.filesystem import FileSensor

from datetime import datetime

start_date = datetime(2023,2,5)
description = "Data pre-processing"
tags = ['sensor']
schedule = '@daily'


with DAG('dag_sensor',
    schedule=schedule,
    start_date=start_date,
    description=description,
    tags=tags
    catchup=False
    ):

    sensor_task = FileSensor(
        task_id='waiting_for_change',
        poke_interval=30,
        # kill sensor if data does
        # not arrive
        timeout= 60 * 5,
        # 'reschedule' or 'poke'
        # the first releases the
        # worker slot in between pokes
        mode='reschedule',
        # skip sensor after timeout
        soft_fail=True,
        filepath= '/tmp/input_data.txt'
    )

    ...