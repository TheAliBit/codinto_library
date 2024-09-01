from rest_framework import serializers
from library.models import BaseRequestModel, BorrowRequest, ExtensionRequest, Review
from library.serializers.book_serializers import FullBookSerializer
from library.serializers.review_serializers import SimpleReviewSerializer
from library.serializers.user_serializers import FullUserSerializer
from library.serializers.Request_serializers import BorrowRequestSerializer, ExtensionRequestSerializer


class AdminRequestSerializer(serializers.ModelSerializer):
    user = FullUserSerializer(read_only=True)
    book = FullBookSerializer(read_only=True)
    request_detail = serializers.SerializerMethodField()

    class Meta:
        model = BaseRequestModel
        fields = [
            'id', 'created_at', 'updated_at', 'request_detail', 'user', 'book'
        ]

    def get_request_detail(self, obj):
        if isinstance(obj, BorrowRequest):
            return BorrowRequestSerializer(obj).data
        elif isinstance(obj, ExtensionRequest):
            return ExtensionRequestSerializer(obj).data
        elif isinstance(obj, Review):
            return SimpleReviewSerializer(obj).data
        elif isinstance(obj, BaseRequestModel):
            return ViewReturnRequestSerializer(obj).data


class ReturnRequestSerializer(serializers.ModelSerializer):
    CHOICES = [('accepted', 'Accepted'), ('pending', 'Pending')]
    status = serializers.ChoiceField(choices=CHOICES, default='pending')
    type = serializers.SerializerMethodField()

    class Meta:
        model = BaseRequestModel
        fields = ['type', 'id', 'status']


class ViewReturnRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = BaseRequestModel
        fields = ['type', 'id', 'status']

    def get_type(self, obj):
        return "return_request"
