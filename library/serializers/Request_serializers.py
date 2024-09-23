from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import BorrowRequest, Book, ExtensionRequest, ReviewRequest, ReturnRequest, BaseRequestModel
from library.serializers.book_serializers import SimpleBookSerializer
from library.serializers.review_serializers import SimpleReviewSerializer


class BookDetailForBorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image']


class BorrowRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRequest
        fields = [
            'type', 'duration', 'start_date', 'end_date'
        ]

    def get_start_date(self, obj):
        return obj.start_date

    def get_type(self, obj):
        return "borrow_request"


class ExtensionRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = ExtensionRequest
        fields = [
            'type', 'duration'
        ]

    def get_type(self, obj):
        return "extension_request"


class ReviewRequestSerializer(serializers.ModelSerializer):
    book = BookDetailForBorrowRequestSerializer()
    request_type = serializers.SerializerMethodField()

    class Meta:
        model = ReviewRequest
        fields = ['request_type', 'id', 'created_at', 'score', 'description', 'book']

    def get_request_type(self, obj):
        return 'ReviewRequest'


class UserRequestSerializer(serializers.Serializer):
    book = SimpleBookSerializer(read_only=True)
    request_detail = serializers.SerializerMethodField()

    class Meta:
        model = BaseRequestModel
        fields = [
            'id', 'created_at', 'updated_at', 'request_detail', 'user', 'book', 'status'
        ]

    def get_request_detail(self, obj):
        if obj.type == 'borrow':
            serializer = BorrowRequestSerializer(obj.borrowrequest)
        elif obj.type == 'extension':
            serializer = ExtensionRequestSerializer(obj.extensionrequest)
        elif obj.type == 'review':
            serializer = SimpleReviewSerializer(obj.reviewrequest)
        elif obj.type == 'return':
            serializer = ViewReturnRequestSerializer(obj.returnrequest)
        else:
            return None

        return serializer.data


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

        if BorrowRequest.objects.filter(user=user, book=book, status='pending').exists():
            raise ValidationError("! شما یک در خواست امانت در جریان دارید, منتظر تعیین وضعیت ادمین باشید")
        elif BorrowRequest.objects.filter(user=user, book=book, is_finished=False).exists():
            raise ValidationError("! شما این کتاب را در اختیار دارید")
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
        fields = ['type']

    # def validate(self, value):
    #     valid_status = ['accepted', 'pending']
    #     if value not in valid_status:
    #         
    #         raise serializers.ValidationError("!وضعیت برای درخواست تحویل نمیتواند رد شود")
    #     
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

        elif ExtensionRequest.objects.filter(user=user, book_id=book, status='accepted').exists():
            raise serializers.ValidationError("! ارسال درخواست تمدید بیشتر از یک بار مجاز نیست")

        return data


class UserReturnRequestSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(required=True, label="امتیاز")
    description = serializers.CharField(required=False, label="متن نظر")

    class Meta:
        model = ReturnRequest
        fields = [
            'id', 'status', 'type', 'score', 'description'
        ]
        read_only_fields = ['status', 'type']

    def validate(self, data):
        user = self.context['request'].user
        book = self.context['view'].kwargs.get('pk')

        if not BorrowRequest.objects.filter(user=user, book_id=book, is_finished=False).exists():
            raise serializers.ValidationError("!شما نمیتوانید کتابی که به امانت نبردید را تحویل دهید")

        elif ReturnRequest.objects.filter(user=user, book_id=book, status='pending').exists():
            raise serializers.ValidationError("!شما یک درخواست تحویل در جریان دارید")

        elif ReturnRequest.objects.filter(user=user, book_id=book, status='accpeted').exists():
            raise serializers.ValidationError("! شما یکبار این کتاب را تحویل دادید")

        elif BaseRequestModel.objects.filter(user=user, book=book, status='pending').exists():
            raise ValidationError("! شما یک درخواست در حال بررسی دارید")
        return data

    def validate_score(self, value):
        if value < 0 or value > 5:
            raise ValidationError("بازه امتیاز از 1 تا 5 است!")
        return value


class BaseRequestSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)

    class Meta:
        model = BaseRequestModel
        fields = [
            'id', 'book', 'duration'
        ]
