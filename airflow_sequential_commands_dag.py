from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'Time_Report',
    default_args=default_args,
    description='A simple sequential command DAG to register hours',
    schedule_interval='55 8 * * *',  # Run every day at 8:55 am
    catchup=True,
)

t1 = BashOperator(
    task_id='run_first_command',
    bash_command='cd /mnt/c/Users/santiago.madariaga/aucs/time-report-bot && powershell.exe -ExecutionPolicy Bypass -File invoke_chrome.ps1',
    dag=dag,
)

t2 = BashOperator(
    task_id='run_second_command',
    bash_command='cd /mnt/c/Users/santiago.madariaga/aucs/time-report-bot && python main.py',
    dag=dag,
)

t3 = BashOperator(
    task_id='run_third_command',
    bash_command='cd /mnt/c/Users/santiago.madariaga/aucs/time-report-bot && powershell.exe -ExecutionPolicy Bypass -File upload.ps1',
    dag=dag,
)

t1 >> t2 >> t3