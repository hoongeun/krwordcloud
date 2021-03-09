#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-

import calendar
import os
import requests
import re
import threading
import locale
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from multiprocessing import Process
from time import sleep
from news_crawler.articleparser import ArticleParser
from news_crawler.exceptions import ResponseTimeout

locale.setlocale(locale.LC_TIME, "ko_KR.UTF-8")

class ArticleCrawler(object):
    def __init__(self, entries: dict, write_handler=None):
        # 모든 section 별 정보가 있는 임시 dict
        #self.temp_categories = {"politics": 100, "economy": 101, "society": 102, "culture": 103, "world": 104, "it": 105, "opinion": 110}
        # 실 적용 dict
        self.categories = {"economy": 101,
                           "society": 102, "culture": 103, "it": 105}
        self.entries = entries
        self.write_handler = write_handler
        self.procs = list()

    @staticmethod
    def make_news_page_url(category_url, category_name, crawled_date):
        made_urls = []
        url = category_url + crawled_date.strftime("%Y%m%d")
        # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
        # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨 (Redirect)
        totalpage = ArticleParser.find_news_totalpage(url + "&page=10000")
        for page in range(1, totalpage + 1):
            made_urls.append(url + "&page=" + str(page))
        return made_urls

    @staticmethod
    def get_url_data(url, max_tries=5):
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                return requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            except requests.exceptions:
                sleep(1)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    # str to isoformat
    

    @staticmethod
    def crawling(self, category_name, crawled_date):
        while(1):
            # Multi Process PID
            print("PID "+str(os.getpid())+" is crawling '" +
                  category_name+"' section on "+str(crawled_date))

            # 기사 url 형식
            url_format = f"http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1={self.categories.get(category_name)}&date="

            # start_year년 start_month월 start_day일의 기사를 수집합니다.
            target_urls = self.make_news_page_url(
                url_format, category_name, crawled_date)

            for url in reversed(target_urls):
                request = self.get_url_data(url)
                document = BeautifulSoup(request.content, "html.parser")

                # html - newsflash_body - type06_headline, type06
                # 각 페이지에 있는 기사들 가져오기
                temp_post = document.select(
                    ".newsflash_body .type06_headline li dl")
                temp_post.extend(document.select(
                    ".newsflash_body .type06 li dl"))

                # 각 페이지에 있는 기사들의 url 저장
                post_urls = []
                for line in temp_post:
                    # 해당되는 page에서 조건에 맞는(end_date 이내) 모든 기사들의 URL을 post_urls 리스트에 넣음
                    d = datetime.strptime(line.find("span", attrs={"class": "date"}).contents[0], "%Y.%m.%d. %p %H:%M")
                    if d > crawled_date:
                        post_urls.append(line.a.get("href"))
                del temp_post

                for content_url in reversed(post_urls):  # 기사 url
                    # 크롤링 대기 시간
                    sleep(0.01)

                    # 기사 HTML 가져옴
                    request_content = self.get_url_data(content_url)

                    try:
                        document_content = BeautifulSoup(
                            request_content.content, "html.parser")
                    except:
                        continue

                    try:
                        # 기사 제목 가져옴
                        tag_headline = document_content.find_all(
                            "h3", {"id": "articleTitle"}, {"class": "tts_head"})
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
                            '<span class="t11">(.*)</span>', request_content.text)[0]
                        d = datetime.strptime(time, "%Y.%m.%d. %p %H:%M")

                        # 데이터 입력
                        self.write_handler((d, category_name, text_company, text_headline, text_sentence, content_url))

                        del time
                        del text_company, text_sentence, text_headline
                        del tag_company
                        del tag_content, tag_headline
                        del request_content, document_content

                    # UnicodeEncodeError
                    except Exception as ex:
                        del request_content, document_content
                        pass

    def start(self):
        # crawling url list를 먼저 생성 후, 각 worker들에게 작업 목록을 던져줌
        for category, last_crawled in self.entries.items():
            self.procs.append(Process(target=self.crawling, args=(
                self, category, last_crawled)))
        for proc in self.procs:
            proc.start()

    def stop(self):
        for proc in self.procs:
            proc.kill()
