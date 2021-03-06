#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-

import calendar
import locale
import os
import requests
import re
import threading
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from multiprocessing import Process
from pyhive import hive
from time import sleep
from .articleparser import ArticleParser
from .exceptions import *

locale.setlocale(locale.LC_TIME, "ko_KR.UTF-8")

class ArticleCrawler(object):
    def __init__(self, target_data, end_date, write_handler=None):
        # 모든 section 별 정보가 있는 임시 dict
        #self.temp_categories = {"politics": 100, "economy": 101, "society": 102, "culture": 103, "world": 104, "it": 105, "opinion": 110}
        # 실 적용 dict
        self.categories = {"economy": 101, "society": 102, "culture": 103, "it": 105}
        self.target_data = target_data
        self.write_handler = write_handler
        self.end_date = end_date
        self.stopper = False

        self.conn = hive.Connection(host="localhost", port=10000, username="hive", password="hive", database="krwordcloud", auth="CUSTOM")
        self.curs = self.conn.cursor()
        
    #write_handler 추출용
    def get_write_handler(self):
        return self.write_handler
      
    @staticmethod
    def make_news_page_url(category_url, category_name, crawling_date):
        made_urls = []
        url = category_url + crawling_date.strftime("%Y%m%d")
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
                return requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
            except requests.exceptions:
                sleep(1)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()
        
    #str to isoformat
    def get_time(self, str_time):
        #str_tims format = yyyy.mm.dd. 오전/오후 h:ss
        div_time = str_time.split(" ")
        text_date = div_time[0].split(".")
        text_time = div_time[2].split(":")
        text_time[0] = int(text_time[0]) - (12 if int(text_time[0]) == 12 else 0)
        text_time[0] += (12 if div_time[1] == "오후"  and text_time[0] < 12 else 0)
        text_datetime = datetime(int(text_date[0]), int(text_date[1]), int(text_date[2]), int(text_time[0]), int(text_time[1]), 0)
        return text_datetime
    
    def insert_db(self, article_list):
        if len(article_list) == 0:
            print("Article data is empty.")
            return
        sql = "INSERT INTO krwordcloud.article (news_date, category, written_time, times_name, headline, contents, url) VALUES "
        for val in article_list:
            sql += f"('{val[0]}', '{val[1]}', '{val[2]}', '{val[3]}', '{val[4]}', '{val[5]}', '{val[6]}'), "
        sql = sql[:-2]
        self.curs.execute(sql)
        self.conn.commit()
        
    #Timer 적용을 위해 만든 불필요한 함수.
    def set_stopper(self):
        self.stopper = True

    def crawling(self, category_name, crawling_date):
        count = 0 #임시로 만든 땜빵 변수. 무조건 위에서 다시 선언할 것.()
        article_list = []
        
        #timer : 3m
        ##Timer 이용에 더 좋은 방법을 공부하기
        timer = threading.Timer(180, self.set_stopper)
        timer.start()
        
        while(1):
            #time over or crawling is done
            if self.stopper is True:
                self.insert_db(article_list)
                print(category_name+" Crawling is Done.")
                self.curs.close()
                self.conn.close()
                return

            # Multi Process PID
            print("PID "+str(os.getpid())+" is crawling '"+category_name+"' section on "+str(crawling_date))
            
            # 기사 url 형식
            url_format = f"http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1={self.categories.get(category_name)}&date="

            # start_year년 start_month월 start_day일의 기사를 수집합니다.
            target_urls = self.make_news_page_url(url_format, category_name, crawling_date)

            for url in reversed(target_urls):                    
                request = self.get_url_data(url)
                document = BeautifulSoup(request.content, "html.parser")

                # html - newsflash_body - type06_headline, type06
                # 각 페이지에 있는 기사들 가져오기
                temp_post = document.select(".newsflash_body .type06_headline li dl")
                temp_post.extend(document.select(".newsflash_body .type06 li dl"))
	
                # 각 페이지에 있는 기사들의 url 저장
                post_urls = []
                for line in temp_post:
                # 해당되는 page에서 조건에 맞는(end_date 이내) 모든 기사들의 URL을 post_urls 리스트에 넣음
                    get_temp_post_time = self.get_time(line.find("span", attrs={"class":"date"}).contents[0])
                    if get_temp_post_time > crawling_date:
                        post_urls.append(line.a.get("href"))
                del temp_post
                
                for content_url in reversed(post_urls):  # 기사 url
                    if count >= 100:
                        self.insert_db(article_list)
                        article_list = []
                        count = 0;
                    else:
                        count += 1
                    # 크롤링 대기 시간
                    sleep(0.01)

                    # 기사 HTML 가져옴
                    request_content = self.get_url_data(content_url)

                    try:
                        document_content = BeautifulSoup(request_content.content, "html.parser")
                    except:
                        continue

                    try:
                        # 기사 제목 가져옴
                        tag_headline = document_content.find_all("h3", {"id": "articleTitle"}, {"class": "tts_head"})
                        # 뉴스 기사 제목 초기화
                        text_headline = ''
                        text_headline = text_headline + ArticleParser.clear_headline(str(tag_headline[0].find_all(text=True)))
                        # 공백일 경우 기사 제외 처리
                        if not text_headline:
                            continue

                        # 기사 본문 가져옴
                        tag_content = document_content.find_all("div", {"id": "articleBodyContents"})
                        # 뉴스 기사 본문 초기화
                        text_sentence = ''
                        text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
                        # 공백일 경우 기사 제외 처리
                        if not text_sentence:
                            continue
                        # 기사 언론사 가져옴
                        tag_company = document_content.find_all("meta", {"property": "me2:category1"})
                        # 언론사 초기화
                        text_company = ''
                        text_company = text_company + str(tag_company[0].get("content"))
                        # 공백일 경우 기사 제외 처리
                        if not text_company:
                            continue

                        # 기사 시간대 가져옴
                        time = re.findall('<span class="t11">(.*)</span>',request_content.text)
                        text_datetime = self.get_time(time[0]).isoformat()

                        # 데이터 입력
                        article_list.append([crawling_date.date(), category_name, text_datetime, text_company, text_headline, text_sentence, content_url])

                        del time
                        del text_company, text_sentence, text_headline
                        del tag_company
                        del tag_content, tag_headline
                        del request_content, document_content

                    # UnicodeEncodeError
                    except Exception as ex:
                        del request_content, document_content
                        pass
            self.insert_db(article_list)
            article_list = []
            count = 0
            crawling_date += timedelta(days=1)
            # 일괄적으로 0시 초기화 시키는 방법이 없나?
            crawling_date = crawling_date.replace(hour=0,minute=0,second=0)
            if crawling_date > self.end_date:
                timer.cancel()
                self.stopper = True
        
    def start(self):
        # MultiProcess 크롤링 시작 ---- 기존 코드가 너무 비효율적. 이후 worker에 작업을 할당하는 형식으로 변경 필요
        for category_name in self.target_data:
            crawling_date = self.target_data.get(category_name)
            proc = Process(target=self.crawling, args=(category_name, crawling_date))
            proc.start()
