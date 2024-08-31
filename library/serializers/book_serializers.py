from rest_framework import serializers
from library.models import Book


class FullBookSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher', 'volume_number', 'publication_year',
            'page_count', 'owner', 'description', 'count', 'category'
        ]
