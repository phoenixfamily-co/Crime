from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('start/', views.start, name='start-view'),  # صفحه اصلی
    path('suspects/', views.suspects, name='suspects-view'),  # صفحه اصلی
    path('interrogation/', views.suspects, name='interrogation-view'),  # صفحه اصلی

]
