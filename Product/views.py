from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.translation import get_language, get_language_bidi
from rest_framework import viewsets

from Product.models import Case, Suspect, Interrogation, Evidence
from Product.serializers import CaseSerializer, SuspectSerializer, InterrogationSerializer, EvidenceSerializer


@cache_page(60 * 15)
def start(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'start.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def suspects(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'suspects.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def interrogation(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'interrogation.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def evidence(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'evidence.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def result(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'result.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def autopsy(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'autopsy.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class SuspectViewSet(viewsets.ModelViewSet):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer


class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer

    def get_queryset(self):
        queryset = Evidence.objects.all()

        # فیلتر کردن براساس نوع مدرک (اختیاری)
        evidence_type = self.request.query_params.get('evidence_type', None)
        if evidence_type:
            queryset = queryset.filter(evidence_type=evidence_type)

        # فیلتر کردن براساس وضعیت مدرک (اختیاری)
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class InterrogationViewSet(viewsets.ModelViewSet):
    queryset = Interrogation.objects.all()
    serializer_class = InterrogationSerializer
