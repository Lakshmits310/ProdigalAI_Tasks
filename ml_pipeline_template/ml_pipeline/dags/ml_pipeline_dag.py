from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'wine_quality_pipeline',
    default_args=default_args,
    description='End-to-end wine quality ML pipeline',
    schedule_interval='@weekly',
    catchup=False,
)

ingest_task = BashOperator(
    task_id='ingest_data',
    bash_command='python /scripts/ingest_data.py',
    dag=dag
)

preprocess_task = BashOperator(
    task_id='preprocess_data',
    bash_command='python /scripts/preprocess.py',  # ⬅️ Updated
    dag=dag
)

feature_task = BashOperator(
    task_id='feature_engineering',
    bash_command='python /scripts/feature_engineering.py',
    dag=dag
)

train_task = BashOperator(
    task_id='train_model',
    bash_command='python /scripts/train_model.py',
    dag=dag
)

ingest_task >> preprocess_task >> feature_task >> train_task
