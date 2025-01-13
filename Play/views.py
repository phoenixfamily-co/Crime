from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from Play.models import CasePlay, GameResult
from Play.serializers import GameResultSerializer, CasePlaySerializer
from Product.models import Suspect
from User.views import get_or_create_temporary_user


class CasePlayViewSet(viewsets.ModelViewSet):
    queryset = CasePlay.objects.all()
    serializer_class = CasePlaySerializer

    def create(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response({"detail": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            get_or_create_temporary_user(request)

        case_play_data = {
            'user': self.request.user.id,
            'status': 'in_progress',
        }

        serializer = self.serializer_class(data=case_play_data)
        serializer.is_valid(raise_exception=True)
        saved_instance = serializer.save()

        request.session['case_play_id'] = saved_instance.id
        request.session.modified = True

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameResultViewSet(viewsets.ModelViewSet):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer

    def create(self, request, *args, **kwargs):
        """
        متد شخصی‌سازی شده برای ایجاد GameResult و پایان بازی.
        """
        # دریافت اطلاعات از درخواست
        case_play_id = request.session.get('case_play_id')  # ID بازی که می‌خواهیم نتیجه‌اش را ثبت کنیم
        suspect_id = request.data.get('suspect')

        try:
            suspect = Suspect.objects.get(id=suspect_id)  # پیدا کردن مظنون
        except Suspect.DoesNotExist:
            return Response({"detail": "suspect not found."}, status=status.HTTP_404_NOT_FOUND)

        status_result = 'success' if suspect.role == 'murderer' else 'failed'

        game_play_data = {
            'gameplay': case_play_id,
            'suspect': request.data.get('suspect'),
            'reason': request.data.get('reason'),
            'status': status_result
        }

        try:
            # بازی را پیدا کنید
            case_play = CasePlay.objects.get(id=case_play_id)
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