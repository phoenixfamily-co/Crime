from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # سایر آدرس‌ها
    path('log-exit/', views.log_exit_time, name='log_exit_time'),
]
