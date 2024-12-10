from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('start/', views.start, name='start-view'),  # صفحه اصلی
]
