from django.urls import path
from data_viewer import views

urlpatterns = [
    path('', views.index,),
    path('view', views.view,),
    path('cpc', views.child_per_center,),
]