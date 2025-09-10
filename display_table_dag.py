import configparser
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from datetime import datetime,timedelta

gcs_bucket="us-east1-gcp-composer-85d92d0a-bucket"
gcs_file="data/config.properties"

hook=GCSHook()
config_data=hook.download(bucket_name=gcs_bucket,object_name=gcs_file) #returns binary data(bytes)
    
config=configparser.ConfigParser()
config.read_string(config_data.decode("utf-8")) #converts bytes to strings
    
project_id = config.get("DEFAULT","project_id")
bucket_name = config.get("DEFAULT","bucket_name")
dataset_name = config.get("DEFAULT","dataset_name")
table_name = config.get("DEFAULT","table_name")
    
print("Project:{}, Bucket:{}, Dataset:{}, Table:{}".format(project_id,bucket_name,dataset_name,table_name))
    
    
default_args={'start_date':airflow.utils.dates.days_ago(0),
               'retries':3,
               'retry_delay':timedelta(minutes=2)
               }
               
with DAG('properties_dag_1',default_args=default_args,schedule_interval='*/30 * * * *',catchup=False) as dag:
    
    display_table=BashOperator(
                task_id='display_table',
                bash_command='bq query --use_legacy_sql=FALSE "SELECT * FROM {}.{}.{} LIMIT 50"'.format(project_id, dataset_name, table_name)
                )
                
display_table