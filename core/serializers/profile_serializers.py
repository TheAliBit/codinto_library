from rest_framework import serializers

from codinto_library import settings
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'telegram_id', 'picture']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['picture'] = settings.DOMAIN + instance.picture.url if instance.picture else None
        return result

    def validate_username(self, value):
        if Profile.objects.filter(username=value).exists():
            raise serializers.ValidationError("!کاربری با این نام کاربری وجود دارد")
        return value
