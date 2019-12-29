from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock_Info

# Create your views here.
def index(request):
    crawling_info_list = Stock_Info.objects.all()
    str = ""
    
    for item in crawling_info_list:
        str += item.name

    context = {"crawling_info_list" : crawling_info_list}

    return render(request, "mainapp/index.html", context)