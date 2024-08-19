from rest_framework import serializers

from codinto_library import settings
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'password', 'first_name', 'last_name', 'phone_number', 'email', 'telegram_id', 'picture']
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'read_only': True}}

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['picture'] = settings.DOMAIN + instance.picture.url if instance.picture else None
        return result
