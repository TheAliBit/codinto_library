from rest_framework import serializers

from library.models import ReviewRequest
from library.serializers.book_serializers import SimpleBookSerializer


class DetailedReviewSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)

    class Meta:
        model = ReviewRequest
        fields = ['id', 'score', 'description', 'book']

    def validate_score(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("!امتیاز باید بین 0 تا 5 باشد")
        else:
            return value

    def update(self, instance, validated_data):
        if validated_data['description'] == instance.description and validated_data['score'] == instance.score:
            return instance
        else:
            validated_data['state'] = 'pending'
            return super().update(instance, validated_data)


class SimpleReviewSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = ReviewRequest
        fields = [
            'type', 'id', 'score', 'description'
        ]

    def get_type(self, obj):
        return "review_request"
