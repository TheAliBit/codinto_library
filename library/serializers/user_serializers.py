from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Profile
from library.models import ReviewRequest, ReturnRequest


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'picture'
        ]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'picture'
        ]


class UserCreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRequest
        fields = [
            'id', 'score', 'description', 'status'
        ]
        read_only_fields = ['status']

    def validate(self, data):

        user = self.context['request'].user
        book = self.context['view'].kwargs.get('pk')

        if ReviewRequest.objects.filter(user=user, book=book).exists():
            raise ValidationError('! شما برای این کتاب نظر ثبت کردید')
        elif not ReturnRequest.objects.filter(user=user, book=book, status='accepted').exists():
            raise ValidationError("! شما ابتدا باید مطالعه این کتاب را به پایان برسانید")
        return data

    def validate_score(self, value):
        if value is None:
            raise ValidationError("! امتیاز نمی‌تواند خالی باشد")
        elif value < 0 or value > 5:
            raise ValidationError("بازه امتیاز از 1 تا 5 است!")
        return value

    def validate_description(self, value):
        if value is None:
            raise ValidationError("! متن نظر نمی‌تواند خالی باشد")
        return value
