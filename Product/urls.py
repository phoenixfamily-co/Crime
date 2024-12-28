from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import SuspectViewSet, CaseViewSet, InterrogationViewSet, EvidenceViewSet

app_name = 'product'

router = DefaultRouter()
router.register(r'cases', CaseViewSet)
router.register(r'suspects', SuspectViewSet)
router.register(r'evidences', EvidenceViewSet)
router.register(r'interrogations', InterrogationViewSet)

urlpatterns = [
    path('start/', views.start, name='start-view'),  # صفحه اصلی
    path('suspects/', views.suspects, name='suspects-view'),  # صفحه اصلی
    path('interrogation/', views.interrogation, name='interrogation-view'),  # صفحه اصلی
    path('evidence/', views.evidence, name='evidence-view'),  # صفحه اصلی
    path('result/', views.result, name='result-view'),  # صفحه اصلی
    path('autopsy/', views.autopsy, name='autopsy-view'),  # صفحه اصلی

    path('api/', include(router.urls)),

]
