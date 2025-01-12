from django.utils import timezone
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.response import Response

from Play.models import CasePlay, GameResult
from Play.serializers import GameResultSerializer
from Product.models import Suspect


def start_case_play(request, user):
    # ثبت لاگ فعالیت
    case_play = CasePlay.objects.create(
        user=user,
        started_at=now(),
        status='in_progress'
    )

    request.session['case_play_id'] = case_play.id

    return case_play


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

        status_result = 'success' if suspect.murder else 'failed'

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
