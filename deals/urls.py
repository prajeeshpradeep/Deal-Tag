from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
]
