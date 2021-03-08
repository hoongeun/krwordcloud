import os
import sys
import locale
from pyhive import hive
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, date, timedelta
from news_crawler.articlecrawler import ArticleCrawler


def start_crawler():
    # crawling_category = ["economy", "society", "culture", "it"]
    crawling_category = ["it"]
    end_date = datetime.now()
    end_date = datetime(2010, 1, 4, 23, 59, 59)

    target_data = {}
    for category in crawling_category:
        last_crawled_date = last_crawled_data(category)
        if last_crawled_date is None:
            target_data[category] = datetime(2010, 1, 2, 0, 0, 0)
        elif last_crawled_date > end_date:
            continue
        else:
            target_data[category] = last_crawled_date

    def write_row_handler():
        pass

    Crawler = ArticleCrawler(target_data, end_date, write_row_handler)
    Crawler.start()


# only use test
""""
def last_crawled_data(category_name):
	output_path = os.path.join(os.getcwd(), "../output")
	if os.path.exists(output_path) is not True:
		return None
	sha_files = list(filter(lambda f: os.path.isfile(os.path.join(output_path,f)) and os.path.splitext(os.path.join(output_path,f))[1] == ".tsv" and os.path.split(os.path.join(output_path,f))[1].split("_")[0] == category_name, os.listdir(output_path)))
	if len(sha_files) == 0:
		return None
	else:
		sha_files.sort(key=lambda name: str(name[len(name)-13:len(name)-5]), reverse=True)
		f = open(os.path.join(output_path, sha_files[0]), "r", encoding="utf-8")
		lines = f.readlines()
		if len(lines) == 0:
			return None
		last_crawled = lines[-1].split("\t")
		con_datetime = datetime.fromisoformat(last_crawled[2])
		return con_datetime
		
#read database
"""


def last_crawled_data(category_name):
    # return None

    conn = hive.Connection(host="localhost", port=10000, username="hive", password="hive", database="krwordcloud",
                           auth="CUSTOM")
    print("db is opened")
    curs = conn.cursor()

    sql = f"SELECT max(written_time) FROM krwordcloud.Article WHERE category = '{category_name}'"
    curs.execute(sql)

    last_crawled = curs.fetchone()

    if last_crawled[0] == None:
        return None
    else:
        print(f"last crawled time of {category_name} is {str(last_crawled[0])}")
        curs.close()
        conn.close()
        return datetime.fromisoformat(str(last_crawled[0]))


dag = DAG(dag_id="article_crawler",
          default_args={
              "owner": "krwordcloud",
              "start_date": datetime(2010, 1, 1)
          },
          schedule_interval="@hourly",
          description="KoreaNewsCrawler", )

crawling_task = PythonOperator(task_id="KoreaNewsCrawler",
                               python_callable=start_crawler,
                               dag=dag)

crawling_task
