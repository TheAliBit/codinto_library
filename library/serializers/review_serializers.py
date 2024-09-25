from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Profile
from core.utils import User
from library.models import ReviewRequest
from library.serializers.book_serializers import SimpleBookSerializer


class DetailedReviewSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)

    class Meta:
        model = ReviewRequest
        fields = ['id', 'score', 'description', 'status', 'book']
        read_only_fields = ['status']

    def validate_score(self, value):
        if value == None:
            raise ValidationError('! فیلد امتیاز نمیتواند خالی باشد')
        if value < 0 or value > 5:
            raise serializers.ValidationError("!امتیاز باید بین 0 تا 5 باشد")
        else:
            return value

    def validate_description(self, value):
        if value == None:
            raise ValidationError("! متن نظر نمیتواند خالی باشد")
        return value


class SimpleReviewSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = ReviewRequest
        fields = [
            'type', 'score', 'description'
        ]

    def get_type(self, obj):
        return "review_request"


class UserNameAndImageForReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'picture', 'first_name', 'last_name'
        ]


class ReviewsSerializerForBooks(serializers.ModelSerializer):
    user = UserNameAndImageForReviewSerializer(read_only=True)

    class Meta:
        model = ReviewRequest
        fields = [
            'id', 'score', 'description', 'user'
        ]
