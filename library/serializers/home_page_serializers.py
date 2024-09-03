from rest_framework import serializers

from codinto_library import settings
from library.models import Book, Review


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + instance.image.url if instance.image else None
        return result


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'score', 'description']


class BookDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher', 'volume_number', 'publication_year',
            'page_count', 'owner', 'description', 'count', 'category', 'reviews'
        ]

    def get_reviews(self, obj):
        accepted_reviews = obj.reviews.filter(state='accepted').select_related('user')
        return ReviewSerializer(accepted_reviews, many=True).data


class BookSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher',
            'volume_number', 'publication_year', 'page_count', 'owner',
            'description', 'count', 'category',
        ]
