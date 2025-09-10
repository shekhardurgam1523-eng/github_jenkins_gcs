import airflow
from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from google.cloud import bigquery

def cust_ds_hist():
    client=bigquery.Client()
    dataset_id='{}.cust_ds_hist'.format(client.project)
    dataset=bigquery.Dataset(dataset_id)
    dataset=client.create_dataset(dataset,timeout=30)
    print(client)
    print(dataset)
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
    
def customer_hist():
    client=bigquery.Client()
    table_id='{}.cust_ds_hist.customer_hist'.format(client.project)
    schema=[
		  bigquery.SchemaField("user_id","INTEGER",mode="REQUIRED"),
          bigquery.SchemaField("age","INTEGER",mode="REQUIRED"),
		  bigquery.SchemaField("gender","STRING",mode="REQUIRED"),
          bigquery.SchemaField("occupation","STRING",mode="REQUIRED"),
          bigquery.SchemaField("zip_code","STRING",mode="REQUIRED"),
		   ]		 
    table = bigquery.Table(table_id,schema=schema)
    table = client.create_table(table)
    print("created {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
    
default_args = {
                'start_date': airflow.utils.dates.days_ago(0),
                'retries':3,
                'retry_delay':timedelta(minutes=5)
                }
                
dag = DAG(
           'task_dag_3',
           default_args=default_args,
           description='dag to ingest data from local to bq',
           schedule_interval='*/40 * * * *',
           catchup=False
           )
         
dummy_start=DummyOperator(
                    task_id='dummy_start'
                    )
                   
create_bucket=BashOperator(
                    task_id='create_bucket',
                    bash_command='gsutil mb gs://cust_bucket_dag',
                    dag=dag
                    )

copy_file=BashOperator(
                    task_id='copy_file',
                    bash_command='gsutil cp gs://practice_bucket-15/customer_details.csv gs://cust_bucket_dag',
                    dag=dag
                    )
                   
create_stg_ds=BashOperator(
                    task_id='create_stg_ds',
                    bash_command='bq mk -d cust_ds_stg',
                    dag=dag
                    )
                    
create_hist_ds=PythonOperator(
                    task_id='create_hist_ds',
                    python_callable=cust_ds_hist,
                    dag=dag
                    )

create_stg_table=BashOperator(
                    task_id='create_stage_table',
                    bash_command='bq mk -t cust_ds_stg.customer_staging user_id:string,age:string,gender:string,occupation:string,zip_code:string',
                    dag=dag
                    )

create_hist_table=PythonOperator(
                    task_id='create_history_table',
                    python_callable=customer_hist,
                    dag=dag
                    )

load_to_stg=BashOperator(
                task_id='load_data_to_stg',
                bash_command='bq load --source_format=CSV --skip_leading_rows=1 cust_ds_stg.customer_staging gs://cust_bucket_dag/customer_details.csv',
                dag=dag
                )
              
insert_to_hist=BashOperator(
                task_id='insert_to_hist',
                bash_command='bq query --use_legacy_sql=FALSE "insert into cust_ds_hist.customer_hist select safe_cast(user_id as int64),safe_cast(age as int64),gender,occupation,zip_code from cust_ds_stg.customer_staging"',
                dag=dag
                )
                    
dummy_end=DummyOperator(
                    task_id='dummy_end'
                    )
                          
dummy_start>>create_bucket>>copy_file>>create_stg_ds>>create_hist_ds>>create_stg_table>>load_to_stg>>create_hist_table>>insert_to_hist>>dummy_end
                    