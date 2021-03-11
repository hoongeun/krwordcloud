import os
import sys
import locale
from threading import Timer
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, date, timedelta
from news_crawler.articlecrawler import ArticleCrawler
from db.presto import PrestoDB


def crawl():
    categories = ["it"]
    # categories = ["economy", "society", "culture", "it"]
    entries = dict()

    presto = PrestoDB(
        host=os.environ.get('TRINO_HOST', 'localhost'),
        port=int(os.environ.get('TRINO_PORT', 8080)),
        user=os.environ.get('TRINO_USER', 'user'),
        password=os.environ.get('TRINO_PASSWORD', 'password'))

    def write_row_handler(row: tuple[datetime, str, str, str, str, str]):
        presto.insert_row(row)

    entries = make_entries(presto, categories)
    crawler = ArticleCrawler(entries, write_row_handler)
    timer = Timer(3540, lambda: (
        timer.cancel(),
        crawler.stop()
    ))
    timer.start()
    try:
        crawler.start()
    except Exception as e:
        print(e)
        crawler.stop()
    presto.close()


def make_entries(presto: PrestoDB, categories: list[str]):
    entries = dict()
    end_date = datetime.now()

    def last_crawled_data(category_name: str):
        cursor = presto.conn.cursor()
        query = f"SELECT max(date) FROM article WHERE category = '{category_name}'"
        cursor.execute(query)
        last_crawled = cursor.fetchone()
        if last_crawled == None or last_crawled[0] == None:
            return None
        else:
            print(
                f"last crawled time of {category_name} is {str(last_crawled[0])}")
            return datetime.fromisoformat(str(last_crawled[0]))

    for category in categories:
        last_crawled_date = last_crawled_data(category)
        if last_crawled_date is None:
            entries[category] = datetime(2010, 1, 1, 0, 0, 0)
        elif last_crawled_date > end_date:
            continue
        else:
            entries[category] = last_crawled_date
    return entries


dag = DAG(dag_id="crawl_articles",
          default_args={
              "owner": "krwordcloud",
              "start_date": datetime(2010, 1, 1)
          },
          schedule_interval="@hourly",
          description="The task to crawl the korean news")

crawl = PythonOperator(task_id="KoreaNewsCrawler",
                       python_callable=crawl,
                       dag=dag)

crawl
