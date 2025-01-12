from rest_framework import serializers

from Play.models import GameResult


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ['gameplay', 'suspect', 'reason', 'status']