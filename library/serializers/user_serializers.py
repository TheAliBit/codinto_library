from rest_framework import serializers

from core.models import Profile


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'telegram_id', 'picture'
        ]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'picture'
        ]
