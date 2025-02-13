from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

# from common.get_data import api_check,get_data
import requests,json
station_id = "ST-10"
def api_check(station_id):
    url = f"http://openapi.seoul.go.kr:8088/584a6e6b54706f703730746f44786b/json/bikeList/1/5/{station_id}" 
    response = requests.get(url)

    if response.status_code == 200:
        print("Connect Success")
        print(f"Status Code : {response.status_code}")
        return True
    print("Connect Fail")
    print(f"Status Code : {response.status_code}")
    return False

def get_data(station_id):
    url = f"http://openapi.seoul.go.kr:8088/584a6e6b54706f703730746f44786b/json/bikeList/1/5/{station_id}" 
    response = requests.get(url)
    data = response.json()
    print(data["rentBikeStatus"]["list_total_count"])

    
with DAG(
    'tutorial',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple tutorial DAG',
    schedule_interval='1 * * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = PythonOperator(
        task_id='health_check',
        python_callable=api_check,
        op_args=[station_id]
    )

    t2 = PythonOperator(
        task_id='get_data',
        depends_on_past=True,
        python_callable=get_data,
        op_args=[station_id]
    )
    

    t1 >> t2