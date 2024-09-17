from django.template.context_processors import request
from rest_framework import serializers
from library.models import Book
from library.utils import calculate_end_date


class FullBookSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher', 'volume_number', 'publication_year',
            'page_count', 'owner', 'description', 'count', 'category'
        ]


class SingleBookUserSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher', 'volume_number', 'publication_year',
            'page_count', 'owner', 'description', 'count', 'category', 'remaining_days'
        ]

    def get_remaining_days(self, obj):
        request = self.context.get('request')
        return calculate_end_date(request, obj.id)


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image'
        ]
