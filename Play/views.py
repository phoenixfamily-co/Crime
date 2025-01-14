from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Play.models import CasePlay, GameResult
from Play.serializers import GameResultSerializer, CasePlaySerializer
from Product.models import Suspect
from User.views import get_or_create_temporary_user, save_user_device_info


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
