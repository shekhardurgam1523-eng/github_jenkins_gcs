"""A liveness prober dag for monitoring composer.googleapis.com/environment/healthy."""
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from airflow.operators.dummy import DummyOperator



default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'bucket_dag_dummy_b41',
    default_args=default_args,
    description='gcsbucket dag',
    schedule_interval='*/12 * * * *',
)

dummy_start = DummyOperator(
    task_id='dummy_start'
    )

# priority_weight has type int in Airflow DB, uses the maximum.
bucket_create = BashOperator(
    task_id='bucket_create',
    bash_command='gsutil mb gs://cdeb41airflowbkt5',
    dag=dag
    )

 

dataset_create = BashOperator(
    task_id='dataset_create',
    bash_command='bq mk -d airflow_b41ds5',
    dag=dag
    )
    
  
dummy_end = DummyOperator(task_id='dummy_end')


dummy_start >> bucket_create >> dataset_create >> dummy_end