from rest_framework import serializers

from library.models import BorrowRequest, Book, ExtensionRequest, Review, ReviewRequest


class BookDetailForBorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image']


class UserBorrowRequestSerializer(serializers.ModelSerializer):
    book = BookDetailForBorrowRequestSerializer()
    request_type = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRequest
        fields = [
            'request_type', 'id', 'created_at', 'duration', 'status', 'book'
        ]

    def get_request_type(self, obj):
        return 'BorrowRequest'


class UserExtensionRequestSerializer(serializers.ModelSerializer):
    book = BookDetailForBorrowRequestSerializer()
    request_type = serializers.SerializerMethodField()

    class Meta:
        model = ExtensionRequest
        fields = [
            'request_type', 'id', 'created_at', 'duration', 'status', 'book'
        ]

    def get_request_type(self, obj):
        return 'ExtensionRequest'


class ReviewRequestSerializer(serializers.ModelSerializer):
    book = BookDetailForBorrowRequestSerializer()
    request_type = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['request_type', 'id', 'created_at', 'score', 'description', 'state', 'book']

    def get_request_type(self, obj):
        return 'ReviewRequest'


class UserRequestSerializer(serializers.Serializer):
    request = serializers.SerializerMethodField()

    class Meta:
        fields = ['request']

    def get_request(self, obj):
        if isinstance(obj, BorrowRequest):
            return UserBorrowRequestSerializer(obj).data
        elif isinstance(obj, ExtensionRequest):
            return UserExtensionRequestSerializer(obj).data
        elif isinstance(obj, Review):
            return ReviewRequestSerializer(obj).data
        else:
            return None


class UserBorrowRequestSerializer_(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = [
            'id', 'time', 'status'
        ]

        read_only_fields = ['status']

    def validate(self, data):
        user = self.context['request'].user
        book = self.context['view'].kwargs.get('pk')


        if BorrowRequest.objects.filter(user=user, book_id=book, status='pending').exists():
            raise serializers.ValidationError("!شما یک درخواست درحال بررسی دارید")
        return data
