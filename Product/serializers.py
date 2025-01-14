from rest_framework import serializers
from .models import Case, Suspect, Interrogation, Evidence, Comment


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'report', 'difficulty_number', 'difficulty_level', 'age_range', 'result'
            , 'price', 'image', 'video']


class SuspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suspect
        fields = ['id', 'name', 'age', 'height', 'weight', 'blood_type', 'marital_status', 'case', 'role',
                  'job', 'gender', 'relationship_with_victim', 'excuse', 'last_seen', 'image', 'video']


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ['id', 'case', 'evidence_type', 'title', 'description', 'file', 'status', 'password',
                  'image', 'details']


class InterrogationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interrogation
        fields = ['id', 'suspect', 'question', 'answer', 'heart_rate', 'face_expression', 'truth_level']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'description', 'score', 'case']

