from rest_framework import serializers
from library.models import BaseRequestModel
from library.serializers.book_serializers import FullBookSerializer
from library.serializers.review_serializers import SimpleReviewSerializer
from library.serializers.user_serializers import FullUserSerializer
from library.serializers.Request_serializers import BorrowRequestSerializer, ExtensionRequestSerializer, \
    ViewReturnRequestSerializer


class AdminRequestSerializer(serializers.ModelSerializer):
    user = FullUserSerializer(read_only=True)
    book = FullBookSerializer(read_only=True)
    request_detail = serializers.SerializerMethodField()

    class Meta:
        model = BaseRequestModel
        fields = [
            'id', 'created_at', 'updated_at', 'request_detail', 'user', 'book', 'status'
        ]

    def get_request_detail(self, obj):
        SERIALIZER_CHOICES = {
            'borrow': BorrowRequestSerializer,
            'extension': ExtensionRequestSerializer,
            'review': SimpleReviewSerializer,
            'return': ViewReturnRequestSerializer
        }
        request_type = obj.type
        serializer_class = SERIALIZER_CHOICES.get(request_type)
        serializer = serializer_class(obj)
        return serializer.data

    def validate_status(self, value):
        valid_status = ['accepted', 'pending']
        request_type = self.initial_data.get('type')
        if value not in valid_status:
            raise serializers.ValidationError("!وضعیت برای درخواست تحویل امکان رد شدن ندارد")
        return value
