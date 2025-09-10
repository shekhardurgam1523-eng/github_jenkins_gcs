from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define DAG
dag = DAG(
    'xcom_example',
    start_date=datetime(2024, 4, 2),
    schedule_interval='@daily',
    catchup=False
)

# Task to push data into XCom
def push_data(**kwargs):
    kwargs['ti'].xcom_push(key='ord_msg', value='weekly task')
    
push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_data,
    provide_context=True,
    dag=dag
)

# Task to pull data from XCom
def pull_data(**kwargs):
    message = kwargs['ti'].xcom_pull(task_ids='push_task', key='ord_msg')
    print(f"Pulled Message: {message}")

pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_data,
    provide_context=True,
    dag=dag
)

# Define task sequence
push_task >> pull_task
