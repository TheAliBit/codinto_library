from rest_framework import serializers

from core.models import Profile
from library.models import ReviewRequest


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


class UserCreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRequest
        fields = '__all__'
