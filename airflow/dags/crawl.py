import os
import traceback
import config
from threading import Timer
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from news_crawler.articlecrawler import ArticleCrawler
from repository.hdfs import HDFS


hdfs = HDFS(
    host=os.environ.get('HDFS_HOST', 'localhost'),
    port=int(os.environ.get('HDFS_PORT', 50070)),
    user=os.environ.get('HDFS_USER', 'hdfs'))
hdfs.connect()


def write_row_handler(rows: list[(datetime, str, str, str, str, str)]):
    hdfs.insert_rows(rows)


def crawl():
    entries = hdfs.make_entries()
    print("entries: ", entries)
    crawler = ArticleCrawler(entries, write_row_handler)
    timer = Timer(config.time_to_live, lambda: (
        timer.cancel(),
        crawler.stop(),
    ))
    timer.start()

    try:
        crawler.start()
    except Exception:
        traceback.print_exc()
        crawler.stop()
    hdfs.save_snapshot()
    hdfs.disconnect()


dag = DAG(dag_id="crawl_articles",
          default_args={
              "owner": "krwordcloud",
              "start_date": datetime(2010, 1, 1)
          },
          schedule_interval="0 */3 * * *",
          description="The task to crawl the korean news")

crawl = PythonOperator(task_id="KoreaNewsCrawler",
                       python_callable=crawl,
                       dag=dag)

crawl()