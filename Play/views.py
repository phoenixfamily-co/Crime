from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import get_language, get_language_bidi
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from CrimeProject.decorators import session_auth_required
from Play.models import CasePlay, GameResult
from Play.serializers import GameResultSerializer, CasePlaySerializer
from Product.models import Suspect, Case, Evidence
from User.views import get_or_create_temporary_user, save_user_device_info, log_user_activity


@session_auth_required
def success(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)
    evidences = Evidence.objects.filter(case=pk)

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'games/success.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'evidences': evidences,
        'activity_log_id': log.id,

    })


@session_auth_required
def failed(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    product = get_object_or_404(Case, id=pk)
    evidences = Evidence.objects.filter(case=pk)

    log = log_user_activity(request, request.build_absolute_uri(), request.user)

    return render(request, 'games/failed.html', {
        'LANGUAGE_CODE': current_language,
        'LANGUAGE_BIDI': is_bidi,
        'case': product,
        'evidences': evidences,
        'activity_log_id': log.id,

    })


class CasePlayViewSet(viewsets.ModelViewSet):
    queryset = CasePlay.objects.all()
    serializer_class = CasePlaySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_or_create_temporary_user(request)

        save_user_device_info(request, user)

        case_play_data = {
            'user': user.id,
            'status': 'in_progress',
        }

        serializer = self.serializer_class(data=case_play_data)
        serializer.is_valid(raise_exception=True)
        saved_instance = serializer.save()

        request.session['play_id'] = saved_instance.id
        request.session.modified = True

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameResultViewSet(viewsets.ModelViewSet):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        متد شخصی‌سازی شده برای ایجاد GameResult و پایان بازی.
        """
        # دریافت اطلاعات از درخواست
        play_id = request.session.get('play_id')  # ID بازی که می‌خواهیم نتیجه‌اش را ثبت کنیم
        suspect_id = request.data.get('suspect')

        try:
            suspect = Suspect.objects.get(id=suspect_id)  # پیدا کردن مظنون
        except Suspect.DoesNotExist:
            return Response({"detail": "suspect not found."}, status=status.HTTP_404_NOT_FOUND)

        status_result = 'success' if suspect.role == 'murderer' else 'failed'

        game_play_data = {
            'gameplay': play_id,
            'suspect': request.data.get('suspect'),
            'reason': request.data.get('reason'),
            'status': status_result
        }

        try:
            # بازی را پیدا کنید
            case_play = CasePlay.objects.get(id=play_id)
        except CasePlay.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=game_play_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        # به‌روزرسانی وضعیت بازی در مدل CasePlay
        case_play.status = 'completed'
        case_play.completed_at = timezone.now()
        case_play.save()

        # بازگشت پاسخ
        return Response(serializer.data, status=status.HTTP_201_CREATED)
