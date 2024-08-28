from rest_framework import serializers

from library.models import Review


class DetailedReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    book = serializers.CharField(source='book.title', read_only=True)

    # state = serializers.CharField(source='review.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'score', 'description', 'state']
        read_only_fields = ['state']

    def validate_score(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError({'message': "!امتیاز باید بین 0 تا 5 باشد"})
        else:
            return value

    def update(self, instance, validated_data):
        if 'description' in validated_data:
            validated_data['state'] = 'pending'
        return super().update(instance, validated_data)
