from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime


with DAG("example_dag", start_date=datetime(2023,2,5), schedule="@daily", catchup=False, description="Training ML models A-C", tags=["training"]):

    @task
    ## simulate training accuracy metric
    def training_model(accuracy):
        return accuracy

    @task.branch
    ## evaluate accuracies and trigger follow-ups
    def best_model(accuracies):
        ### find best accuracy
        best_accuracy = max(accuracies)
        ### trigger next step based on value
        if (best_accuracy > 7):
            return 'acc_passed'
        return 'acc_failed'

    acc_passed = BashOperator(
        task_id="acc_passed",
        bash_command="echo 'INFO :: Accuracy assessment PASSED minimum requirements'"
    )

    acc_failed = BashOperator(
        task_id="acc_failed",
        bash_command="echo 'WARNING :: Accuracy assessment FAILED minimum requirements'"
    )

    best_model(training_model.expand(accuracy=[3, 7, 9])) >> [acc_passed, acc_failed]