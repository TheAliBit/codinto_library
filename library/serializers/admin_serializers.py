from multiprocessing.managers import public_methods

from rest_framework import serializers
from library.models import BaseRequestModel, Notification
from library.serializers.book_serializers import FullBookSerializer, SimpleBookSerializer
from library.serializers.review_serializers import SimpleReviewSerializer
from library.serializers.user_serializers import FullUserSerializer, SimpleUserSerializer
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
            serializer = SimpleReviewSerializer(obj)
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
