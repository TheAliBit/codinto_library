from rest_framework import serializers
from codinto_library import settings
from library.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'children']
        read_only_fields = ['children']

    # Custom validation
    def validate(self, data):
        title = data.get('title')
        if Category.objects.filter(title=title).exists():
            raise serializers.ValidationError({'message': '!دسته بندی تکراری است'})
        return data

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + instance.image.url if instance.image else None
        return result
