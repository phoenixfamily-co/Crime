from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GameResultViewSet, CasePlayViewSet

app_name = 'play'

router = DefaultRouter()
router.register(r'result', GameResultViewSet)
router.register(r'start', CasePlayViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]