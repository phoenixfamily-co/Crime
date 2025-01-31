from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # سایر آدرس‌ها
    path('log-exit/', views.log_exit_time, name='log_exit_time'),
    path("user-observe/", views.UserObserve.as_view(), name="list_user"),
    path("user-observe/<str:number>/", views.UserObserve.as_view(), name="detail_user"),
    path("user-update/<str:number>/", views.UpdateUser.as_view()),
]
