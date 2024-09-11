from rest_framework import serializers

from library.models import Notification


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'description', 'image'
        ]
