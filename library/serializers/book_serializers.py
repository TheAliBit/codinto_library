from rest_framework import serializers
from library.models import Book


class FullBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'translator', 'publisher', 'volume_number', 'publication_year', 'page_count',
            'owner', 'description', 'count', 'category'
        ]
