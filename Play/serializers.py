from rest_framework import serializers

from Play.models import GameResult, CasePlay


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ['gameplay', 'suspect', 'reason', 'status']

    def create(self, validated_data):
        return GameResult.objects.create(**validated_data)


class CasePlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CasePlay
        fields = ['user', 'status']

    def create(self, validated_data):
        return CasePlay.objects.create(**validated_data)
