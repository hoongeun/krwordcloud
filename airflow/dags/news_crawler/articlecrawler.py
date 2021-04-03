#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-

import os
import requests
import re
import config
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathos import multiprocessing
from time import sleep
from news_crawler.articleparser import ArticleParser
from news_crawler.exceptions import ResponseTimeout
from news_crawler import utils


categories = {"economy": 101, "society": 102, "culture": 103, "it": 105}


class ArticleCrawler(object):
    def __init__(self, entries: dict, write_handler=None):
        self.entries = entries
        self.write_handler = write_handler
        self.procs = list()
        self.status = 'active'

    @staticmethod
    def make_news_page_url(entries):
        urls = []
        sdate = min(entries.values()).date()
        edate = datetime.now()
        delta = edate.date() - sdate
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            print('crawl date: ', day)
            for category, last_crawled in entries.items():
                if last_crawled.date() <= day:
                    # lastpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 lastpage를 알아냄
                    # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=lastpage로 이동 됨
                    # (Redirect)
                    url = "http://news.naver.com/main/list.nhn?mode=LSD&" + \
                          f"mid=sec&sid1={categories.get(category)}" + \
                          f"&date={day.strftime('%Y%m%d')}&page=10000"
                    totalpage = ArticleParser.find_news_totalpage(url)
                    for page in reversed(range(1, totalpage + 1)):
                        urls.append((category, (f"{url}&page={page}")))
            yield urls
            urls = []
        return list(urls)

    @staticmethod
    def request_url(url, max_tries=5):
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                return requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            except requests.exceptions:
                sleep(1)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    @staticmethod
    def crawling(article_urls: list[(str, str)]):
        rows = []
        # Multi Process PID
        print(f"PID {str(os.getpid())} is crawling "
              f"{len(article_urls)} articles")

        for category, url in article_urls:  # 기사 url
            # 크롤링 대기 시간
            sleep(0.01)

            # 기사 HTML 가져옴
            response = ArticleCrawler.request_url(url)

            try:
                document_content = BeautifulSoup(
                    response.content, "html.parser")
            except Exception:
                continue

            try:
                # 기사 제목 가져옴
                tag_headline = document_content.find_all(
                    "h3", {"id": "articleTitle"},
                    {"class": "tts_head"})
                if len(tag_headline) == 0:
                    continue
                # 뉴스 기사 제목 초기화
                text_headline = ArticleParser.clear_headline(
                    str(tag_headline[0].find_all(text=True)))
                # 공백일 경우 기사 제외 처리
                if not text_headline:
                    continue
                # 기사 본문 가져옴
                tag_content = document_content.find_all(
                    "div", {"id": "articleBodyContents"})
                if len(tag_content) == 0:
                    continue
                # 뉴스 기사 본문 초기화
                text_sentence = ArticleParser.clear_content(
                    str(tag_content[0].find_all(text=True)))
                # 공백일 경우 기사 제외 처리
                if not text_sentence:
                    continue
                # 기사 언론사 가져옴
                tag_company = document_content.find_all(
                    "meta", {"property": "me2:category1"})
                if len(tag_content) == 0:
                    continue
                # 언론사 초기화
                text_company = str(tag_company[0].get("content"))
                # 공백일 경우 기사 제외 처리
                if not text_company:
                    continue
                # 기사 시간대 가져옴
                time = re.findall(
                    '<span class="t11">(.*)</span>',
                    response.text)[0]
                d = utils.parse_datetime(time)
                # print((d, category, text_company,
                #                     text_headline, text_sentence,
                #                     url))
                # 데이터 입력
                rows.append((d, category, text_company,
                             text_headline, text_sentence, url))
            # UnicodeEncodeError
            except Exception:
                continue
        return rows
        # return json.dumps(rows)

    def articles_sequence(self, procs: int):
        result = []
        # start_year년 start_month월 start_day일의 기사를 수집합니다.
        for urls in ArticleCrawler.make_news_page_url(self.entries):
            article_urls = []
            for category, url in urls:
                response = self.request_url(url)
                document = BeautifulSoup(response.content, "html.parser")
                # html - newsflash_body - type06_headline, type06
                # 각 페이지에 있는 기사들 가져오기
                flahses = document.select(
                    ".newsflash_body .type06_headline li dl")
                flahses.extend(document.select(
                    ".newsflash_body .type06 li dl"))
                new_flashes = filter(lambda x: utils.parse_datetime(
                    x.find("span", attrs={"class": "date"}).contents[0])
                    > self.entries[category], flahses)
                # 각 페이지에 있는 기사들의 url 저장
                page_article_urls = list(
                    map(lambda flash: (category, flash.a.get('href')),
                        new_flashes))
                article_urls.extend(page_article_urls)
            for i in range(0, len(article_urls), config.queue_size):
                urls_per_proc = article_urls[i:i+config.queue_size]
                result.append(urls_per_proc)
                if len(result) >= procs:
                    yield result
                    result.clear()
            yield result
            result.clear()
        return result

    def start(self):
        # consider hyper-threaing
        self.status = 'active'
        self.run()

    def run(self):
        procs = config.procs or (multiprocessing.cpu_count() - 1)
        self.pool = multiprocessing.ProcessPool(nodes=procs)
        for articles in self.articles_sequence(procs=procs):
            results = self.pool.map(ArticleCrawler.crawling, articles)
            for rows in list(results):
                self.write_handler(rows)
            if self.status != 'active':
                self.status = 'terminated'
                break
            self.pool.restart()

    def stop(self, force=False):
        self.status = 'terminating'
        if force:
            self.pool.terminate()
