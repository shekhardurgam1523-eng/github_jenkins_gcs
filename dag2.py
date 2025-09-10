import airflow
from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator


default_args={
               'start_date':airflow.utils.dates.days_ago(0),
               'retries':3,
               'retry_delay':timedelta(minutes=10)
               }
               
dag2=DAG(
        'dag-2',
        default_args=default_args,
        description='dag2 for trigger dag example',
        schedule_interval=None,
        catchup=False
        )
        
dummy_start=DummyOperator(task_id='dummy_start')  

copy_file=BashOperator(
                task_id='copy_file',
                bash_command='gsutil cp gs://practice_bucket-15/customer_details.csv gs://bucket_trigger_op',
                dag=dag2
                )
                
              
dummy_stop=DummyOperator(task_id='dummy_stop')

dummy_start>>copy_file>>dummy_stop
               