from django.shortcuts import render
from django.utils.translation import get_language, get_language_bidi
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Product.models import Case, Suspect, Interrogation, Evidence, Comment
from Product.serializers import CaseSerializer, SuspectSerializer, InterrogationSerializer, EvidenceSerializer, \
    CommentSerializer
from User.models import User
from User.views import get_or_create_temporary_user, log_user_activity
from CrimeProject.decorators import *
from CrimeProject.permissions import *


def play(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)

    if request.user.is_authenticated:
        user = request.user
    else:
        user = get_or_create_temporary_user(request)

    log = log_user_activity(request, request.build_absolute_uri(), user)

    return render(request, 'play.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'activity_log_id': log.id,

    })


@session_auth_required
def start(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'start.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'activity_log_id': log.id,

    })


@session_auth_required
def suspects(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)
    suspect = Suspect.objects.filter(case=pk).exclude(role='murdered')

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'suspects.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'suspects': suspect,
        'activity_log_id': log.id,

    })


@session_auth_required
def interrogation(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    interrogations = Interrogation.objects.filter(suspect=pk)
    suspect = get_object_or_404(Suspect, id=pk)

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'interrogation.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'interrogations': interrogations,
        'suspect': suspect,
        'activity_log_id': log.id,

    })


@session_auth_required
def evidence(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)
    evidences = Evidence.objects.filter(case=pk)

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'evidence.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'evidences': evidences,
        'activity_log_id': log.id,

    })


@session_auth_required
def result(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = Case.objects.get(id=pk)
    suspect = Suspect.objects.filter(case=pk)

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'result.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'suspect': suspect,
        'activity_log_id': log.id,

    })


@session_auth_required
def autopsy(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    report = get_object_or_404(Evidence, id=pk)
    suspect = get_object_or_404(Suspect, case=report.case.pk, role='murdered')

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'autopsy.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'suspect': suspect,
        'evidence': report,
        'activity_log_id': log.id,

    })


@session_admin_required
def create_case(request):
    current_language = get_language()
    is_bidi = get_language_bidi()

    return render(request, 'manager/create_case.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
    })


@session_admin_required
def create_suspect(request):
    current_language = get_language()
    is_bidi = get_language_bidi()
    cases = Case.objects.all()

    return render(request, 'manager/create_suspect.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'cases': cases,

    })


@session_admin_required
def create_evidence(request):
    current_language = get_language()
    is_bidi = get_language_bidi()
    cases = Case.objects.all()

    return render(request, 'manager/create_evidence.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'cases': cases,
    })


@session_admin_required
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
    permission_classes = [IsAdminOrStaff]

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
    permission_classes = [IsAdminOrStaff]

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
    permission_classes = [IsAdminOrStaff]

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
    permission_classes = [IsAdminOrStaff]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # دریافت داده‌ها از درخواست
        data = request.data.copy()  # کپی داده‌های موجود
        user = User.objects.get(id=self.request.user.id)
        user.first_name = data['name']
        user.last_name = data['family']
        user.number = data['number']
        user.save()
        data['user'] = user
        serializer = self.get_serializer(data=data)

        # اعتبارسنجی و ذخیره داده‌ها
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)  # داده‌ها ذخیره شده و پاسخ برگشت می‌دهیم
        return Response(serializer.errors, status=400)
