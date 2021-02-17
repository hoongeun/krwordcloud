from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import date, datetime
from crawler import crawling

dag = DAG(dag_id='news_data_task',
          owner='krwordcloud',
          email=['airflow@example.com'],
          email_on_failure=False,
          email_on_retry=False,
          schedule_interval='@hourly')

start = datetime(2010, 1, 1, 0, 0, 0, 0001)
end = date.today()

crawlingTask = PythonOperator(
    dag=dag,
    task_id='crawl_the_korean_news',
    python_callable=crawling,
    op_kwargs={'startyear': start.year(),
               'startmonth': start.month(),
               'endyear': end.year(),
               'endmonth': end.month()},
)


def datamining():


miningTask = PythonOperator(
    task_id='data_mining_from_news',
    op_kwargs={'output': '/'}
    python_callable=crawling,
    dag=dag
)

crawlingTask >> miningTask
