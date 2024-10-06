from rest_framework import serializers
from library.models import Category


class SimpleCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent']

    def validate_parent(self, value):
        if self.instance:  # Ensure we're updating, not creating
            if value == self.instance:
                raise serializers.ValidationError('! کتگوری نمی تواند زیرکتگوری خودش باشد')
        return value

    def validate_title(self, value):
        if self.instance:  # Ensure we're updating, not creating
            if value == self.instance.title:
                raise serializers.ValidationError('! عنوان کتگوری تکراری است')
        return value


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

    # # Custom validation
    # def validate(self, data):
    #     title = data.get('title')
    #     if Category.objects.filter(title=title).exists():
    #         raise serializers.ValidationError({'message': '!دسته بندی تکراری است'})
    #     return data


class SingleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent']
