from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from codinto_library import settings
from core.urls import urlpatterns
from library.models import Book, ReviewRequest, Notification
from library.serializers.book_serializers import FullBookSerializer
from library.serializers.user_serializers import FullUserSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'image']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + instance.image.url if instance.image else None
        return result


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ReviewRequest
        fields = ['id', 'username', 'score', 'description']


class BookDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher', 'volume_number', 'publication_year',
            'page_count', 'owner', 'description', 'count', 'category', 'reviews'
        ]

    def get_reviews(self, obj):
        accepted_reviews = obj.reviews.filter(state='accepted').select_related('user')
        return ReviewSerializer(accepted_reviews, many=True).data


class BookListSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher',
            'volume_number', 'publication_year', 'page_count', 'owner',
            'description', 'count', 'category',
        ]

    def validate_title(self, value):
        if Book.objects.filter(title=value).exists():
            raise ValidationError("!کتابی با این نام موجود هست")
        return value


class BookSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher',
            'volume_number', 'publication_year', 'page_count', 'owner',
            'description', 'count', 'category',
        ]

    def validate_title(self, value):
        if Book.objects.filter(title=value).exists():
            raise ValidationError("!کتابی با این نام موجود هست")
        return value


class BookAvailableRemainderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = []

    def validate(self, attrs):
        user = self.context['request'].user
        book = self.context['view'].kwargs.get('pk')
        if Notification.objects.filter(user=user, book=book).exists():
            raise ValidationError('! شما یکبار درخواست موجود شد به من اطلاع بدید رو انتخاب کردید')
        return attrs
