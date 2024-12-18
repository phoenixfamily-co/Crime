from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home-view'),  # صفحه اصلی
    path('not/supprt/', views.home, name='support-view'),  # صفحه اصلی

]
