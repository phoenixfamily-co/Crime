from django.urls import path
from . import views

urlpatterns = [
    # سایر آدرس‌ها
    path('log-exit/', views.log_exit_time, name='log_exit_time'),
]
