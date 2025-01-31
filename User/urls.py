from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # سایر آدرس‌ها
    path('log-exit/', views.log_exit_time, name='log_exit_time'),
    path("userview/", views.UserView.as_view(), name="list_user"),
    path("userview/<str:number>/", views.UserView.as_view(), name="detail_user"),
]
