from rest_framework import serializers

from library.models import Review


class DetailedReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    book = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'score', 'description', 'state']

# class DetailedReviewSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source='user.name', read_only=True)
#     book = serializers.CharField(source='book.title', read_only=True)
#
#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'book', 'score', 'description', 'state']
