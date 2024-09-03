from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from codinto_library import settings
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'telegram_id', 'picture']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['picture'] = settings.DOMAIN + instance.picture.url if instance.picture else None
        return result


class AdminListProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'telegram_id', 'picture']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['picture'] = settings.DOMAIN + instance.picture.url if instance.picture else None
        return result

    def validate_username(self, value):
        if Profile.objects.filter(username=value).exists():
            raise ValidationError("!کاربری با این نام کاربری وجود دارد")
        return value

    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise ValidationError("!کاربری با این ایمیل وجود دارد")
        return value

    def validate_phone_number(self, value):
        if Profile.objects.filter(phone_number=value).exists():
            raise ValidationError("!کاربری با این شماره تلفن وجود دارد")
        return value

    def validate_telegram_id(self, value):
        if Profile.objects.filter(telegram_id=value).exists():
            raise ValidationError("!کاربری با این آیدی تلگرام وجود دارد")
        return value


class AdminSingleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'telegram_id']

    def validate_username(self, value):
        if value and Profile.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!این نام کاربری برای کاربر دیگری است")
        return value

    def validate_email(self, value):
        if value and Profile.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!کاربری دیگر با این ایمیل وجود دارد")
        return value

    def validate_phone_number(self, value):
        if value and Profile.objects.filter(phone_number=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!این شماره تلفن مربوط به یک پروفایل دیگر است")
        return value

    def validate_telegram_id(self, value):
        if value and Profile.objects.filter(telegram_id=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!این آیدی برای شخص دیگریست")
        return value
