
import sys
sys.path.append("/opt/airflow/")  # Add the parent directory to the Python path

from pipeline.pipeline import fetch_and_store
from airflow import DAG
from airflow.operators.python import PythonOperator 
from datetime import datetime



with DAG(
    dag_id='testin_dag',
    start_date=datetime(2026, 1, 1),
    schedule_interval='*/1 * * * *',
    catchup=False
) as dag:
    task1 = PythonOperator(
        task_id="crypto_pipeline",
        python_callable= fetch_and_store
    )

    