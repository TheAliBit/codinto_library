from rest_framework import serializers

from library.models import Review
from library.serializers.book_serializers import SimpleBookSerializer


class DetailedReviewSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'score', 'description', 'state', 'book']
        read_only_fields = ['state']

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
    class Meta:
        model = Review
        fields = ['id', 'score', 'description', 'state']
