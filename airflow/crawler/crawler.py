from korea_news_crawler.articlecrawler import ArticleCrawler


def crawling(startyear: int, startmonth: int, endyear: int, endmonth: int):
    Crawler = ArticleCrawler()
    Crawler.set_category("생활문화", "IT과학", "경제", "사회")
    Crawler.set_date_range(startyear, startmonth, endyear, endmonth)
    Crawler.start()
