from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.translation import get_language, get_language_bidi
from rest_framework import viewsets
from rest_framework.response import Response

from Product.models import Case, Suspect, Interrogation, Evidence
from Product.serializers import CaseSerializer, SuspectSerializer, InterrogationSerializer, EvidenceSerializer


@cache_page(60 * 15)
def start(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = Case.objects.get(id=pk)

    return render(request, 'start.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product
    })


@cache_page(60 * 15)
def suspects(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = Case.objects.filter(id=pk)

    return render(request, 'suspects.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product

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
def evidence(request,pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = Case.objects.filter(id=pk)

    return render(request, 'evidence.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product

    })


@cache_page(60 * 15)
def result(request,pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = Case.objects.filter(id=pk)

    return render(request, 'result.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product

    })


@cache_page(60 * 15)
def autopsy(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'autopsy.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def create_case(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'manager/create_case.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@cache_page(60 * 15)
def create_suspect(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'manager/create_suspect.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


def create_evidence(request):
    current_language = get_language()
    is_bidi = get_language_bidi()
    cases = Case.objects.all()

    return render(request, 'manager/create_evidence.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'cases': cases,
    })


def create_interrogation(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'manager/create_interrogation.html', {
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

    def create(self, request, *args, **kwargs):
        # دریافت داده‌ها از درخواست
        data = request.data.copy()  # کپی داده‌های موجود
        file = request.FILES.get('file')  # دریافت فایل از request.FILES

        # اگر فایل وجود داشته باشد، آن را به داده‌ها اضافه می‌کنیم
        if file:
            data['file'] = file

        serializer = self.get_serializer(data=data)

        # اعتبارسنجی و ذخیره داده‌ها
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # داده‌ها ذخیره شده و پاسخ برگشت می‌دهیم
        return Response(serializer.errors, status=400)


class InterrogationViewSet(viewsets.ModelViewSet):
    queryset = Interrogation.objects.all()
    serializer_class = InterrogationSerializer
