from django.shortcuts import render
from django.http import HttpResponse
from .models import Crawling_Data
import logging

LOGGER = logging.getLogger("DEBUG")
# Create your views here.
def index(request):
    LOGGER.debug("#########index#########")
    #Crawling_Data().init_crawling_data()

    crawling_list = Crawling_Data.objects.all()

    context = {"crawling_list" : crawling_list}

    return render(request, "mainapp/index.html", context)

#현재 시점으로 크롤링 & 주식 정보 추출하기
def insert_crawling_data(request):
    LOGGER.debug("#########insert_crawling_data#########")

    Crawling_Data().init_crawling_data()

    crawling_list = Crawling_Data.objects.all()

    context = {"crawling_list" : crawling_list}
    
    return render(request, "mainapp/index.html", context)

#전체 데이터 삭제
def delete_all(request):
    LOGGER.debug("#########delete_all#########")
    Crawling_Data().delete_all()

    return render(request, "mainapp/index.html")