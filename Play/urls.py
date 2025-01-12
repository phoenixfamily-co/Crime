from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Play.views import GameResultViewSet

app_name = 'play'


router = DefaultRouter()
router.register(r'result', GameResultViewSet)


urlpatterns = [
    path('api/', include(router.urls)),

]