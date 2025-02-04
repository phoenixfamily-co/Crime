from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ProfileView
app_name = 'login'

# router = DefaultRouter()
# router.register(r'register', RegisterView, basename='register')



urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    # path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
#     path("userview-list/", UserObserve.as_view(), name="list_user"),
#     path("userview-detail/<int:pk>/", UserObserve.as_view(), name="list_user"),
]
