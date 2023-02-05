from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime
from random import randint

# define functions to be run by airflow
## simulate training accuracy metric
def _training_model():
    return randint(1,10)

## evaluate accuracies and trigger follow-ups
def _best_model(ti):
    ### get results from training runs
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    ### find best accuracy
    best_accuracy = max(accuracies)
    ### trigger next step based on value
    if (best_accuracy > 7):
        return 'acc_passed'
    return 'acc_failed'



with DAG("example_dag", start_date=datetime(2023,2,5), schedule="@daily", catchup=False, description="Training ML models A-C", tags=["modelA", "modelB", "modelC", "training"]) as dag:

    training_model_A = PythonOperator(
        task_id="training_model_A",
        python_callable=_training_model
    )

    training_model_B = PythonOperator(
        task_id="training_model_B",
        python_callable=_training_model
    )

    training_model_C = PythonOperator(
        task_id="training_model_C",
        python_callable=_training_model
    )

    choose_best_model = BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=_best_model
    )

    acc_passed = BashOperator(
        task_id="acc_passed",
        bash_command="echo 'INFO :: Accuracy assessment PASSED minimum requirements'"
    )

    acc_failed = BashOperator(
        task_id="acc_failed",
        bash_command="echo 'WARNING :: Accuracy assessment FAILED minimum requirements'"
    )

    ## define task flow
    [training_model_A, training_model_B, training_model_C] >> choose_best_model >> [acc_passed, acc_failed]