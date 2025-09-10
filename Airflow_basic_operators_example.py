
DummyOperator/EmptyOperator: This operator is a do-nothing operator and it is often used to create a step in a workflow that has no action associated with it. Here is an example:
----------------------
from airflow.operators.dummy import DummyOperator

dummy_operator = DummyOperator(task_id='dummy_task')

The DummyOperator in Airflow is a do-nothing operator that is often used to create a step in a workflow that has no action associated with it. It is useful for a few different purposes:

Placeholder tasks: DummyOperator can be used as a placeholder task in a workflow. For example, you might have a workflow where you want to create a task that represents a manual intervention or approval step. In this case, you can use a DummyOperator as a placeholder for that step.

EmptyOperator

Visualizing workflows: DummyOperator can be used to add visual separation between tasks in a workflow. By adding a DummyOperator between two tasks, you can create a visual separation that makes the workflow easier to read and understand.
Grouping tasks: DummyOperator can be used to group tasks together in a workflow. For example, you might have a workflow where you want to group a set of tasks together and give them a common label. In this case, you can use a DummyOperator to create a grouping task with a descriptive name.


PythonOperator: This operator allows you to run a Python function as part of a workflow. Here is an example:
----------------------
from airflow.operators.python_operator import PythonOperator

def my_python_function():
    print('Hello, Airflow!')

python_operator = PythonOperator(
    task_id='python_task', 
    python_callable=my_python_function
)


BranchPythonOperator: allows you to dynamically determine the next task to be executed based on the result of a Python function:

from airflow.operators.python_operator import BranchPythonOperator

def my_branch_function():
    if(date = 30 or date = 31)
      some_branch_name = yes
    return some_branch_name

branch_operator = BranchPythonOperator(
    task_id='branch_task',
    python_callable=my_branch_function,
)
--------------------------

Hook: Airflow provides hooks to interact with external systems. Here is an example of a SlackHook:
----------------------
from airflow.hooks.slack_hook import SlackHook

slack_hook = SlackHook(slack_conn_id='my_slack_conn')
slack_hook.send_message('Hello, Slack!')

Sensor: A sensor is an operator that waits for a certain condition to be true before moving on to the next task. Here is an example of a TimeSensor:
----------------------
from airflow.sensors.time_sensor import TimeSensor

time_sensor = TimeSensor(task_id='wait_for_5_seconds', timeout=5)

ShortCircuitOperator: This operator allows you to skip tasks based on the result of a Python function. Here is an example:
----------------------
from airflow.operators.short_circuit import ShortCircuitOperator

def my_short_circuit_function():
    return some_condition

short_circuit_operator = ShortCircuitOperator(
task_id='short_circuit_task', 
python_callable=my_short_circuit_function)


*******
Google Cloud Storage Operators:

GoogleCloudStorageCreateBucketOperator This operator creates a new bucket in GCS. Example:
    
     
    
----------------------
create_bucket = GoogleCloudStorageCreateBucketOperator(
    task_id='create_bucket',
    bucket_name='my-new-bucket',
 )
 
 
GoogleCloudStorageDeleteObjectsOperator This operator deletes objects from a GCS bucket. Example:

----------------------
delete_objects = GoogleCloudStorageDeleteObjectsOperator(
    task_id='delete_objects',
    bucket='my-bucket',
    objects=['object1', 'object2'],
    google_cloud_storage_conn_id='my_conn'
)

   
GoogleCloudStorageDownloadFileOperator This operator downloads a file from GCS to a local file path. Example:

----------------------
download_file = GoogleCloudStorageDownloadFileOperator(
    task_id='download_file',
    source_bucket='my-bucket',
    source_object='my-file',
    destination_path='/path/to/local/file',
    google_cloud_storage_conn_id='my_conn'
)

BigQuery Operators:
-------------------

BigQueryCreateEmptyTableOperator This operator creates an empty table in BigQuery. Example:
----------------------
create_table = BigQueryCreateEmptyTableOperator(
    task_id='create_table',
    dataset_id='my_dataset',
    table_id='my_table',
    schema_fields=[
        {"name": "emp_name", "type": "STRING", "mode": "REQUIRED"},
        {"name": "salary", "type": "INTEGER", "mode": "NULLABLE"},
    ],
    bigquery_conn_id='my_conn'
)

BigQueryInsertJobOperator This operator runs a BigQuery SQL query. Example:
----------------------
insert_query_job = BigQueryInsertJobOperator(
    task_id='insert_query_job',
    configuration={
        "query": {
            "query": "SELECT * FROM my_dataset.my_table",
            "useLegacySql": False,
        }
    },
    bigquery_conn_id='my_conn'
)

BigQueryGetDataOperator This operator retrieves data from a BigQuery table. Example:
----------------------
get_data = BigQueryGetDataOperator(
    task_id='get_data',
    dataset_id='my_dataset',
    table_id='my_table',
    selected_fields="value,name",
    bigquery_conn_id='my_conn'
)


BigQueryUpsertTableOperator This operator upserts data into a BigQuery table. Example:
----------------------
upsert_table = BigQueryUpsertTableOperator(
    task_id='upsert_table',
    dataset_id='my_dataset',
    table_resource={
        "tableReference": {
            "tableId": "my_table"
        },
        "schema": {
            "fields": [
                {
                    "name": "emp_name",
                    "type": "STRING",
                    "mode": "REQUIRED"
                },
                {
                    "name": "salary",
                    "type": "INTEGER",
                    "mode": "NULLABLE"
                }
            ]
        }
    },
    bigquery_conn_id='my_conn'
)

BigQueryDeleteTableOperator This operator deletes a BigQuery table. Example:
----------------------
delete_table = BigQueryDeleteTableOperator(
    task_id='delete_table',
    deletion_dataset_table='my_dataset.my_table',
    bigquery_conn_id='my_conn'
)


--------------------------------------------------
Dependency with another DAG:
-------------------------------

trigger_dag2 = TriggerDagRunOperator(
    task_id='trigger_dag2',
    trigger_dag_id='dag2',
    dag=dag,
)

task1 >> task2 >> trigger_dag2

-------------------------------------------