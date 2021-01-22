from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

from datetime import date
from krwordrank.word import KRWordRank
import krwordrank
from wordcloud import WordCloud

args = {'owner': 'jovyan', 'start_date': days_ago(n=1)}
dag = DAG(dag_id='news_crawler',
          default_args=args,
          schedule_interval='@daily')


today = date.today()

crawlingTask = PythonOperator(
    dag=dag,
    task_id='crawl_the_korean_news',
    python_callable=crawling,
    op_kwargs={'startyear': today.year(), 'startmonth': today.month(
    ), 'endyear': today.year(), 'endmonth': today.month()},
)


def datamining():


miningTask = PythonOperator(
    task_id='data_mining_from_news',
    op_kwargs={'output': '/'}
    dag=dag
)

crawlingTask >> miningTask
