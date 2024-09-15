from rest_framework import serializers

from library.models import BorrowRequest, Book, ExtensionRequest, Review, ReturnRequest, BaseRequestModel
from library.serializers.book_serializers import SimpleBookSerializer


class BookDetailForBorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image']


class BorrowRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRequest
        fields = [
            'type', 'id', 'duration', 'status', 'start_date'
        ]

    def get_type(self, obj):
        return "borrow_request"


class ExtensionRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = ExtensionRequest
        fields = [
            'type', 'id', 'duration', 'status'
        ]

    def get_type(self, obj):
        return "extension_request"


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
            return BorrowRequestSerializer(obj).data
        elif isinstance(obj, ExtensionRequest):
            return ExtensionRequestSerializer(obj).data
        elif isinstance(obj, Review):
            return ReviewRequestSerializer(obj).data
        else:
            return None


class UserBorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = [
            'id', 'time', 'status', 'type'
        ]
        read_only_fields = ['status', 'type']

    def validate(self, data):
        user = self.context['request'].user
        book = self.context['view'].kwargs.get('pk')

        if BorrowRequest.objects.filter(user=user, book_id=book, status='accepted').exists():
            raise serializers.ValidationError("!این کتاب را شما در حال حاظر در اختیار دارید")
        elif BorrowRequest.objects.filter(user=user, book_id=book, status='pending').exists():
            raise serializers.ValidationError("!شما یک درخواست درحال بررسی دارید")
        return data


class ReturnRequestSerializer(serializers.ModelSerializer):
    CHOICES = [('accepted', 'Accepted'), ('pending', 'Pending')]
    status = serializers.ChoiceField(choices=CHOICES, default='pending')
    type = serializers.SerializerMethodField()

    class Meta:
        model = ReturnRequest
        fields = ['type', 'id', 'status']

    def get_type(self, obj):
        return "return_request"


class ViewReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = ['type', 'id', 'status']

    # def validate(self, value):
    #     valid_status = ['accepted', 'pending']
    #     if value not in valid_status:
    #         print('1')
    #         raise serializers.ValidationError("!وضعیت برای درخواست تحویل نمیتواند رد شود")
    #     print('1')
    #     return value


class UserExtensionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtensionRequest
        fields = [
            'id', 'time', 'status', 'type'
        ]
        read_only_fields = ['status', 'type']

    def validate(self, data):
        user = self.context['request'].user
        book = self.context['view'].kwargs.get('pk')

        if not BorrowRequest.objects.filter(user=user, book_id=book, status='accepted').exists():
            raise serializers.ValidationError("!شما درحال حاظر درخواست امانت درجریانی ندارید")

        elif ExtensionRequest.objects.filter(user=user, book_id=book, status='pending').exists():
            raise serializers.ValidationError("!شما یک درخواست درحال بررسی دارید")

        return data


class UserReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = [
            'id', 'status', 'type'
        ]
        read_only_fields = ['status', 'type']

    def validate(self, data):
        user = self.context['request'].user
        book = self.context['view'].kwargs.get('pk')

        if not BorrowRequest.objects.filter(user=user, book_id=book, status='accepted').exists():
            raise serializers.ValidationError("!شما نمیتوانید کتابی که به امانت نبردید را تحویل دهید")
        elif ReturnRequest.objects.filter(user=user, book_id=book, status='pending').exists():
            raise serializers.ValidationError("!شما یک درخواست تحویل در جریان دارید")
        elif ReturnRequest.objects.filter(user=user, book_id=book, status='accpeted').exists():
            raise serializers.ValidationError("! شما یکبار این کتاب را تحویل دادید")
        return data


class BaseRequestSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)

    class Meta:
        model = BaseRequestModel
        fields = [
            'id', 'book', 'duration'
        ]
