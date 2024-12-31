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
    path('start/<int:pk>/', views.start, name='start-view'),  # صفحه اصلی
    path('suspects/<int:pk>/', views.suspects, name='suspects-view'),  # صفحه اصلی
    path('interrogation/<int:pk>/', views.interrogation, name='interrogation-view'),  # صفحه اصلی
    path('evidence/<int:pk>/', views.evidence, name='evidence-view'),  # صفحه اصلی
    path('result/<int:pk>/', views.result, name='result-view'),  # صفحه اصلی
    path('autopsy/', views.autopsy, name='autopsy-view'),  # صفحه اصلی
    path('manager/case/', views.create_case, name='create-case-view'),  # صفحه اصلی
    path('manager/suspect/', views.create_suspect, name='creat-suspect-view'),  # صفحه اصلی
    path('manager/evidence/', views.create_evidence, name='create-evidence-view'),  # صفحه اصلی
    path('manager/interrogation/', views.create_interrogation, name='create-interrogation-view'),  # صفحه اصلی

    path('api/', include(router.urls)),

]
