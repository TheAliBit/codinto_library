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
