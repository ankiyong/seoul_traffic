from datetime import datetime, timedelta
from textwrap import dedent
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from datetime import datetime
import requests,json

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models.variable import Variable

station_id = "ST-10"
api_key = Variable.get("API_KEY")
address = Variable.get("URL")
def api_check(station_id):
    url = f"{address}/{api_key}/json/bikeList/1/5/{station_id}" 
    response = requests.get(url)

    if response.status_code == 200:
        print("Connect Success")
        print(f"Status Code : {response.status_code}")
        return True
    print("Connect Fail")
    print(f"Status Code : {response.status_code}")
    return False

def get_data(station_id):
    url = f"{address}/{api_key}/json/bikeList/1/5/{station_id}" 
    response = requests.get(url)
    data = response.json()
    return data["rentBikeStatus"]

    

with DAG(
    'data_pipeline',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple data_pipeline DAG',
    schedule_interval='1 * * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    t1 = PythonOperator(
        task_id='health_check',
        python_callable=api_check,
        op_args=[station_id]
    )

    t2 = PythonOperator(
        task_id='get_data',
        depends_on_past=False,
        python_callable=get_data,
        op_args=[station_id]
    )
    ping_task = BashOperator(
        task_id="ping_google",
        bash_command="ping -c 4 google.com"
    )


    ping_task