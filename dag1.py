import airflow
from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args={
               'start_date':airflow.utils.dates.days_ago(0),
               'retries':3,
               'retry_delay':timedelta(minutes=10)
               }
               
dag1=DAG(
        'dag-1',
        default_args=default_args,
        description='dag1 for trigger dag example',
        schedule_interval='*/20 * * * *',
        catchup=False
        )
        
dummy_start=DummyOperator(task_id='dummy_start')  

create_bucket=BashOperator(
                    task_id='create_bucket',
                    bash_command='gsutil mb gs://trigger_dag_bucket_1',
                    dag=dag1
                    )
                    
trigger_dag=TriggerDagRunOperator(
                    task_id='copy_file',
                    trigger_dag_id='dag-2',
                    dag=dag1
                    )
                    
dummy_stop=DummyOperator(task_id='dummy_stop')

dummy_start>>create_bucket>>trigger_dag>>dummy_stop