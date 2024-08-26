from rest_framework import serializers

from codinto_library import settings
from library.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + instance.image.url if instance.image else None
        return result
