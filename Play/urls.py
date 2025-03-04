from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GameResultViewSet, CasePlayViewSet, success , failed

app_name = 'play'

router = DefaultRouter()
router.register(r'result', GameResultViewSet)
router.register(r'start', CasePlayViewSet)

urlpatterns = [
    path('success/<int:pk>/', success, name='success-view'),  # صفحه اصلی
    path('failed/<int:pk>/', failed, name='failed-view'),  # صفحه اصلی

    path('api/', include(router.urls)),
]