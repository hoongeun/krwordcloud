import pandas as pd
from hdfs import InsecureClient
from pyspark.sql import SparkSession
from krwordrank.word import KRWordRank
from kafka import KafkaProducer
import json
import os
from typing import Iterator
from filter import filter_stopwords

producer = None

if os.environ.get("KAFKA_HOST") and os.environ.get("KAFKA_PORT"):
    host = os.environ.get("KAFKA_HOST")
    port = os.environ.get("KAFKA_PORT")
    producer = KafkaProducer(
        acks=0,
        compression_type="gzip",
        bootstrap_servers=[f"{host}:{port}"],
        value_serializer=lambda x: json.dumps(x).encode("        print(data)utf-8"),
    )

spark = SparkSession.builder.master("local").appName("krwordcloud").getOrCreate()
sc = spark.sparkContext

hdfs = InsecureClient(
    f"http://{os.environ.get('HDFS_HTTP_HOST', 'localhost')}:{os.environ.get('HDFS_HTTP_PORT', 14000)}",
    user=os.environ.get("HDFS_USER", "hdfs"),
)


def generate_input(articles):
    result = []

    def split(string):
        return list(
            string.replace("다. ", "다.\n")
            .replace("음. ", "음.\n")
            .replace("함. ", "함.\n")
            .replace("임. ", "임.\n")
            .split("\n")
        )

    for article in articles:
        result.extend(split(article["title"]) * 3)  # to add weight(x3)
        result.extend(split(article["content"]))
    return result


for _f in hdfs.list("/krwordcloud/add-article"):
    df = spark.read.orc(
        f"hdfs://{os.environ.get('HDFS_HOST', 'localhost')}:{os.environ.get('HDFS_PORT', 8020)}/krwordcloud/add-article/{_f}"
    )
    ndf = df.groupBy("category", "press").agg(
        F.collect_list(F.struct("title", "content")).alias("articles")
    )

    def mapper(row: pd.Series):
        extractor = KRWordRank(
            min_count=7,  # Minimum word occurrence
            max_length=15,  # Maximum word length
            verbose=False,
        )
        beta = 0.85  # decaying factor beta of PageRank
        max_iter = 10

        sentences = generate_input(row["articles"])

        try:
            score, rank, graph = extractor.extract(sentences, beta, max_iter)
            score = dict(filter(filter_stopwords, score.items()))
        except Exception as e:
            print(e)
            return None

        return dict(
            {
                "date": os.path.splitext(_f)[0],
                "press": row["press"],
                "category": row["category"],
                "size": len(" ".join(sentences).encode("utf8")),
                "score": score,
                "rank_size": len(rank),
                "graph_size": len(graph),
            }
        )

    for data in ndf.rdd.map(mapper).filter(lambda x: x is not None).collect():
        if producer:
            producer.send("add-trend", value=data)
