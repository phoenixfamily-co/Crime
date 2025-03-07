from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'podcast'

router = DefaultRouter()
router.register(r'podcast', PodcastViewSet, basename='podcast')

urlpatterns = [
    path('', PodcastViewSet.as_view(), name='podcast-view'),  # صفحه اصلی
    path('blog/<int:pk>/', PodcastPostDetailView.as_view(), name='podcast-detail'),

    path('api/', include(router.urls)),

]
