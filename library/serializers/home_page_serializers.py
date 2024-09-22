from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import jdatetime

from codinto_library import settings
from core.models import Profile
from library.models import Book, ReviewRequest, Notification, Category


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
    owner = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    count = serializers.SerializerMethodField()
    # category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source='category'
    )
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher',
            'volume_number', 'publication_year', 'page_count', 'owner',
            'description', 'count', 'category_id', 'categories'
        ]
        extra_kwargs = {'category': {'required': True}}

    def get_count(self, obj):
        if obj.count > 0:
            return 'is_available'
        else:
            return 'is_not_available'

    def validate_title(self, value):
        if Book.objects.filter(title=value).exists():
            raise ValidationError("!کتابی با این نام موجود هست")
        return value

    def validate_publication_year(self, value):
        current_shamsi_year = jdatetime.datetime.now().year
        print(current_shamsi_year)
        if value < 1300:
            raise ValidationError("! تاریخ انتشار نمیتواند زمانی قبل تر از سال 1300 باشد")
        elif value > current_shamsi_year:
            raise ValidationError("! تاریخ انتشار نمیتواند زمانی بعد تر از تاریخ حال حاظر باشد")
        else:
            return value

    def validate_category(self, value):
        if not value:
            raise ValidationError("! کتگوری الزامیست")
        return value

    def get_categories(self, obj):
        def build_hierarchy(category):
            if category is None:
                return None
            return {
                'id': category.id,
                'title': category.title,
                'parent': build_hierarchy(category.parent)
            }

        return build_hierarchy(obj.category)


class BookSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author', 'translator', 'publisher',
            'volume_number', 'publication_year', 'page_count', 'owner',
            'description', 'count', 'category',
        ]

    def validate_title(self, value):
        if not self.instance:
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
        if Notification.objects.filter(user=user, book=book, type='available').exists():
            raise ValidationError('! شما یکبار درخواست موجود شد به من اطلاع بدید رو انتخاب کردید')
        return attrs
