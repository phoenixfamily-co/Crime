from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.translation import get_language, get_language_bidi
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from Product.models import Case, Suspect, Interrogation, Evidence
from Product.serializers import CaseSerializer, SuspectSerializer, InterrogationSerializer, EvidenceSerializer


@cache_page(60 * 15)
def play(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)

    return render(request, 'play.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product
    })


@cache_page(60 * 15)
def start(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)

    return render(request, 'start.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product
    })


@cache_page(60 * 15)
def suspects(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)
    suspect = Suspect.objects.filter(case=pk).exclude(role='murdered')

    return render(request, 'suspects.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'suspects': suspect,

    })


@cache_page(60 * 15)
def interrogation(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    interrogations = Interrogation.objects.filter(suspect=pk)
    suspect = get_object_or_404(Suspect, id=pk)

    return render(request, 'interrogation.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'interrogations': interrogations,
        'suspect': suspect
    })


@cache_page(60 * 15)
def evidence(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)
    evidences = Evidence.objects.filter(case=pk)

    return render(request, 'evidence.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'evidences': evidences,

    })


@cache_page(60 * 15)
def result(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = Case.objects.get(id=pk)
    suspect = Suspect.objects.filter(case=pk)

    return render(request, 'result.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'suspect': suspect

    })


@cache_page(60 * 15)
def autopsy(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    report = get_object_or_404(Evidence, id=pk)
    suspect = get_object_or_404(Suspect, case=report.case.pk, role='murdered')
    return render(request, 'autopsy.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'suspect': suspect,
        'evidence': report
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
    cases = Case.objects.all()

    return render(request, 'manager/create_suspect.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'cases': cases,

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
    suspect = Suspect.objects.all

    return render(request, 'manager/create_interrogation.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'suspect': suspect,
    })


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def create(self, request, *args, **kwargs):
        # دریافت داده‌ها از درخواست
        data = request.data.copy()  # کپی داده‌های موجود
        image = request.FILES.get('image')  # دریافت فایل از request.FILES
        video = request.FILES.get('video')  # دریافت فایل از request.FILES

        if image:
            data['image'] = image

        if video:
            data['video'] = video

        serializer = self.get_serializer(data=data)

        # اعتبارسنجی و ذخیره داده‌ها
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # داده‌ها ذخیره شده و پاسخ برگشت می‌دهیم
        return Response(serializer.errors, status=400)


class SuspectViewSet(viewsets.ModelViewSet):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer

    def create(self, request, *args, **kwargs):
        # دریافت داده‌ها از درخواست
        data = request.data.copy()  # کپی داده‌های موجود
        image = request.FILES.get('image')  # دریافت فایل از request.FILES
        video = request.FILES.get('video')  # دریافت فایل از request.FILES

        if image:
            data['image'] = image

        if video:
            data['video'] = video

        serializer = self.get_serializer(data=data)

        # اعتبارسنجی و ذخیره داده‌ها
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # داده‌ها ذخیره شده و پاسخ برگشت می‌دهیم
        return Response(serializer.errors, status=400)


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
        image = request.FILES.get('image')

        # اگر فایل وجود داشته باشد، آن را به داده‌ها اضافه می‌کنیم
        if file:
            data['file'] = file

        if image:
            data['image'] = image

        serializer = self.get_serializer(data=data)

        # اعتبارسنجی و ذخیره داده‌ها
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # داده‌ها ذخیره شده و پاسخ برگشت می‌دهیم
        return Response(serializer.errors, status=400)


class InterrogationViewSet(viewsets.ModelViewSet):
    queryset = Interrogation.objects.all()
    serializer_class = InterrogationSerializer
