from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('date_range/', views.date_range, name='date_range'),
]