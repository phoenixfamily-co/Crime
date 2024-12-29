from rest_framework import serializers
from .models import Case, Suspect, Interrogation, Evidence


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'price']


class SuspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suspect
        fields = ['id', 'name', 'age', 'height', 'weight', 'blood_type', 'status', 'case', 'suspect_interrogations']


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ['id', 'crime_case', 'suspect', 'evidence_type', 'description', 'date_collected', 'file', 'status']



class InterrogationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interrogation
        fields = ['id', 'suspect', 'crime_case', 'question', 'answer', 'heart_rate', 'face_expression', 'truth_level']