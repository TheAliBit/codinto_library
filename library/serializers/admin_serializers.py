from rest_framework import serializers

from core.models import Profile
from library.models import BaseRequestModel, Notification, BorrowRequest, Book, ReturnRequest
from library.serializers.book_serializers import FullBookSerializer
from library.serializers.home_page_serializers import BookSerializer
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

    def validate_status(self, value):
        valid_status = ['accepted', 'pending']
        request_type = self.instance.type if self.instance else self.initial_data.get('type')

        if self.instance.status != 'pending':
            raise serializers.ValidationError(
                '! شما یک بار وضعیت در خواست را رد و یا تایید کردید و دیگر این امکان برای شما فراهم نیست')

        if request_type == 'return' and value not in valid_status:
            raise serializers.ValidationError("!وضعیت برای درخواست تحویل امکان رد شدن ندارد")
        return value


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title', 'description', 'image']

    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_superuser:
            validated_data['type'] = 'public'
        return super().create(validated_data)


class HistoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username']


class HistoryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'image']


class BorrowHistorySerializer(serializers.ModelSerializer):
    user = HistoryUserSerializer(read_only=True)
    book = HistoryBookSerializer(read_only=True)
    retrun_date = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRequest
        fields = ['book', 'user', 'start_date', 'end_date', 'retrun_date']

    def get_retrun_date(self, obj):
        user = obj.user
        book = obj.book
        return_request = ReturnRequest.objects.filter(
            user=user,
            book=book,
            status='accepted'
        ).first()
        if return_request:
            return return_request.updated_at
        return {"درحال مطالعه"}
