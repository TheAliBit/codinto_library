from rest_framework import serializers
from library.models import Book
from library.utils import calculate_end_date

class FullBookSerializerForAdminRequest(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image' , 'count', 'category'
        ]

    def get_count(self, obj):
        if obj.count > 0:
            return 'is_available'
        else:
            return 'is_not_available'

class FullBookSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher', 'volume_number', 'publication_year',
            'page_count', 'owner', 'description', 'count', 'category'
        ]

    def get_count(self, obj):
        if obj.count > 0:
            return 'is_available'
        else:
            return 'is_not_available'


class SingleBookUserSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    remaining_days = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher', 'volume_number', 'publication_year',
            'page_count', 'owner', 'description', 'count', 'category', 'remaining_days'
        ]

    def get_count(self, obj):
        if obj.count > 0:
            return 'is_available'
        else:
            return 'is_not_available'

    def get_remaining_days(self, obj):
        request = self.context.get('request')
        return calculate_end_date(request, obj.id)


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image'
        ]
