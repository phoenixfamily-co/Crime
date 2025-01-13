from rest_framework import serializers

from Play.models import GameResult, CasePlay
from User.models import User


class CasePlaySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,  # فیلد اختیاری
        allow_null=True
    )

    class Meta:
        model = CasePlay
        fields = ['user', 'status']

    def create(self, validated_data):
        return CasePlay.objects.create(**validated_data)


class GameResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameResult
        fields = ['gameplay', 'suspect', 'reason', 'status']

    def create(self, validated_data):
        return GameResult.objects.create(**validated_data)
