from rest_framework import serializers
from library.models import Book, Review


class BookSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    cover_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_image', 'review_count']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
