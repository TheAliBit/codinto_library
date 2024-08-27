from rest_framework import serializers

from library.models import Review


class ReviewSerializer_(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    book = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'book', 'score', 'description', 'state'
        ]


