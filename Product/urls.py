from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('start/', views.start, name='start-view'),  # صفحه اصلی
    path('suspects/', views.suspects, name='suspects-view'),  # صفحه اصلی
    path('interrogation/', views.interrogation, name='interrogation-view'),  # صفحه اصلی
    path('result/', views.result, name='result-view'),  # صفحه اصلی

]
