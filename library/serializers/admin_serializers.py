from rest_framework import serializers
from core.utils import User
from library.models import Book, BorrowRequest, ExtensionRequest, Review


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']


class AdminBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']
        read_only_fields = ['id', 'title']


class AdminBorrowRequestSerializer(serializers.ModelSerializer):
    book = AdminBookSerializer(read_only=True)
    request_type = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRequest
        fields = ['request_type', 'id', 'created_at', 'duration', 'status', 'book']

    def get_request_type(self, obj):
        return 'BorrowRequest'


class AdminExtensionRequestSerializer(serializers.ModelSerializer):
    book = AdminBookSerializer(read_only=True)
    request_type = serializers.SerializerMethodField()

    class Meta:
        model = ExtensionRequest
        fields = ['request_type', 'id', 'created_at', 'duration', 'status', 'book']

    def get_request_type(self, obj):
        return 'ExtensionRequest'


class AdminReviewRequestSerializer(serializers.ModelSerializer):
    book = AdminBookSerializer(read_only=True)
    request_type = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['request_type', 'id', 'created_at', 'score', 'description', 'state', 'book']

    def get_request_type(self, obj):
        return 'ReviewRequest'


class AdminRequestSerializer(serializers.Serializer):
    request = serializers.SerializerMethodField()

    def get_request(self, obj):
        if isinstance(obj, BorrowRequest):
            serializer = AdminBorrowRequestSerializer(obj)
        elif isinstance(obj, ExtensionRequest):
            serializer = AdminExtensionRequestSerializer(obj)
        elif isinstance(obj, Review):
            serializer = AdminReviewRequestSerializer(obj)
        else:
            return None
        return serializer.data
