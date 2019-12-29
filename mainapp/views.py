from django.shortcuts import render
from django.http import HttpResponse
from .models import Crawling_Data
import logging

LOGGER = logging.getLogger("DEBUG")
# Create your views here.
def index(request):
    LOGGER.debug("#########index#########")
    Crawling_Data().init_crawling_data()

    crawling_list = Crawling_Data.objects.all()

    context = {"crawling_list" : crawling_list}

    return render(request, "mainapp/index.html", context)