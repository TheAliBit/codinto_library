from rest_framework import serializers
from library.models import BaseRequestModel, BorrowRequest, ExtensionRequest, Review, ReturnRequest
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
            'id', 'created_at', 'updated_at', 'type', 'request_detail', 'user', 'book'
        ]

    def get_request_detail(self, obj):
        if isinstance(obj, BorrowRequest):
            return BorrowRequestSerializer(obj).data
        elif isinstance(obj, ExtensionRequest):
            return ExtensionRequestSerializer(obj).data
        elif isinstance(obj, Review):
            return SimpleReviewSerializer(obj).data
        elif isinstance(obj, ReturnRequest):
            return ViewReturnRequestSerializer(obj).data
