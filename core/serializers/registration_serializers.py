from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True, label="نام کاربری")
    password = serializers.CharField(max_length=255, required=True, label="رمزعبور", write_only=True)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError({'message': "!کاربری بااین نام کاربری در سامانه وجود ندارد"})
        else:
            return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError({'message': "!رمزعبور باید حداقل 8 کاراکتر باشد"})
        else:
            return value

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError({'message': "!شماره تلفن یا رمزعبور اشتباه است"})
        else:
            return data


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=2500, required=True, label='رفرش توکن')

    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except Exception as e:
            raise serializers.ValidationError({'message': '!توکن نامعتبر است'})
        return value
