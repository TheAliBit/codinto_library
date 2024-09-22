from rest_framework import serializers
from codinto_library import settings
from library.models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'children']
        read_only_fields = ['children']

    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return CategorySerializer(children, many=True).data
        return None

    # Custom validation
    def validate(self, data):
        title = data.get('title')
        if Category.objects.filter(title=title).exists():
            raise serializers.ValidationError({'message': '!دسته بندی تکراری است'})
        return data
