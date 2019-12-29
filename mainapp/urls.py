from django.urls import path
from django.conf.urls import include
from . import views


urlpatterns = [
    path(''                     , views.index               ),
    path('select_crawling_data' , views.index               ),
    path('insert_crawling_data' , views.insert_crawling_data),
    path('delete_all'           , views.delete_all          ),
]
