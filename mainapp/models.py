from django.db import models
from bs4 import BeautifulSoup
import requests
import pandas
import time
import re
import datetime
import logging

LOGGER = logging.getLogger("DEBUG")

#크롤링 한 데이터 Class
class Crawling_Data(models.Model):
    objects = models.Manager()
    company_code = models.CharField(max_length=6)
    company_name = models.CharField(max_length=15)
    news_title = models.TextField(null=True)
    current_time = models.DateTimeField(null=True)
    current_price = models.CharField(null=True, max_length=15)
    indecrease_amount = models.CharField(null=True, max_length=15)
    indecrease_percent = models.CharField(null=True, max_length=15)

    #한경
    URL_HANKYUNG = "http://stock.hankyung.com/news/app/newslist.php?cid=0103"

    def init_crawling_data(self):
        crawling_data = self.make_crawling_data()
        crawling_data = self.add_stock_info(crawling_data)

        for data in crawling_data:
            record = Crawling_Data(company_code=data["company_code"]
            ,company_name= data["company_name"]
            ,news_title= data["news_title"]
            ,current_time= data["current_time"]
            ,current_price= data["current_price"]
            ,indecrease_amount= data["indecrease_amount"]
            ,indecrease_percent= data["indecrease_percent"])
            record.save()
        

    #기사 크롤링
    def get_news_data(self, url_raw_data):
        LOGGER.debug("#########기사 크롤링#########")

        result_list = []
        source_code_from_url = requests.get(url_raw_data)
        source_code_from_url.encoding = "euc-kr"
        soup = BeautifulSoup(source_code_from_url.text, "html.parser")
        li_items = soup.find_all("li", {"class" : "list_news_item"})
        to_date = datetime.date.today()  

        #오늘 날짜 기사만 추출
        for item in li_items:
            item_date = item.find("span", {"class":"list_news_info"}).string
            item_date = datetime.datetime.strptime(item_date.split(" ")[0],"%Y-%m-%d").date()
            
            if to_date - datetime.timedelta(2) <= item_date:
                result_list.append(item.find("strong", {"class":"list_news_sbj"}).string)

        return result_list
        
    #주식 전체 종목 가져오기
    def get_stock_list(self):
        LOGGER.debug("#########주식 전체 종목 가져오기#########")

        table = pandas.read_html("http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13")[0]
        table = table[["회사명","종목코드"]]
        table["종목코드"] = table["종목코드"].map('{0:06d}'.format)
        
        table = table.values.tolist()

        return table
        
    #회사코드 & 회사명 & 기사제목 DataFrame 생성
    def make_crawling_data(self):
        LOGGER.debug("#########회사코드 & 회사명 & 기사제목 DataFrame 생성#########")
        stock_list = self.get_stock_list()
        raw_data_hankyung = self.get_news_data(self.URL_HANKYUNG)
        title_list = []
        result_list = []
        
        #기사제목에서 쌍따옴표 내 제목 추출
        for raw_data in raw_data_hankyung:
            raw_data = raw_data.string
            if "\"" in raw_data:
                title_list.append(raw_data[raw_data.find("\"")+1:raw_data.rfind("\"")])
        
        #회사명 & 기사제목 추출
        for item in stock_list:
            company_name = item[0]
            company_code = item[1]
            for title in title_list:
                if re.search(r"\b" + re.escape(company_name) + r"\b", title):
                    data = {"company_code" : company_code, "company_name" : company_name, "news_title" : title}
                    result_list.append(data)
                    break

        
        return result_list

    #실시간 주가 가져오기
    def add_stock_info(self, company_list):
        LOGGER.debug("#########실시간 주가 가져오기#########")
        now = datetime.datetime.now()
        
        for company in company_list:
            company_code = company["company_code"]
            source_code_from_url = requests.get("https://finance.naver.com/item/main.nhn?code="+company_code)
            source_code_from_url.encoding = "euc-kr"
            soup = BeautifulSoup(source_code_from_url.text, "html.parser")
            current_price = soup.find("p", {"class":"no_today"})
            indecrease_percent = soup.find("p", {"class":"no_exday"})
            if not indecrease_percent.find("span", {"class":"ico plus"}):
                company["indecrease_amount"] = "-" + indecrease_percent.find_all("span", {"class":"blind"})[0].string
                company["indecrease_percent"] = "-" + indecrease_percent.find_all("span", {"class":"blind"})[1].string
            else:
                company["indecrease_amount"] = "+" + indecrease_percent.find_all("span", {"class":"blind"})[0].string
                company["indecrease_percent"] = "+" + indecrease_percent.find_all("span", {"class":"blind"})[1].string

            company["current_price"] = current_price.find("span", {"class":"blind"}).string
            company["current_time"] = "%s-%s-%s %s:%s:%s" %(now.year, now.month, now.day, now.hour, now.minute, now.second)

        return company_list

    