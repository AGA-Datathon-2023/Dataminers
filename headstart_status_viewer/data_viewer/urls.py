from django.urls import path
from data_viewer import views
from data_viewer import api

urlpatterns = [
    path('', views.index,),
    path('view', views.view,),
    path('download', api.API.download,),
]