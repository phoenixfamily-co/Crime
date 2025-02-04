# project/Login/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from User.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()






class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['number', 'password', 'password2', "first_name", "last_name"]

    def validate(self, data):
        # Check if 'number' is provided
        if 'number' not in data or not data['number']:
            raise serializers.ValidationError({"number": "Phone number is required."})
        # Check password match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        try:
            user = User.objects.create_user(**validated_data)

        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

        return user


class LoginSerializer(serializers.Serializer):
    number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(number=data['number'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        }



