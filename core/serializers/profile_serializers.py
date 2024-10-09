from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from codinto_library import settings
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'telegram_id', 'picture', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Add password here as write-only

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['picture'] = settings.DOMAIN + instance.picture.url if instance.picture else None
        return result

    def validate_phone_number(self, value):
        if len(value) != 11:
            raise ValidationError("! شماره تلفن باید متشکل از 11 عدد باشد")

        if not value.startswith('09'):
            raise ValidationError("! شماره تلفن باید با 09 شروع شود")

        # Check for unique phone numbers (uncomment if needed)
        # if Profile.objects.filter(phone_number=value).exclude(id=self.instance.id).exists():
        #     raise ValidationError("! کاربری با این شماره تلفن وجود دارد")

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')  # Fix typo in 'password'
        user = Profile(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def create(self, validated_data):
        passwrod = validated_data.pop('password')
        user = Profile(**validated_data)
        user.set_password(passwrod)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class AdminListProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11,
                                         validators=[RegexValidator(regex=r'^09\d{9}$',
                                                                    message="! طول شماره تلفن باید 11 عدد باشد و با 09 شروع شود")])

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
        if len(value) != 11:
            raise ValidationError("! شماره تلفن باید متشکل از 11 عدد باشد")

        if not value.startswith('09'):
            raise ValidationError("! شماره تلفن باید با 09 شروع شود")

        if Profile.objects.filter(phone_number=value).exists():
            raise ValidationError("!کاربری با این شماره تلفن وجود دارد")

        return value

    def validate_telegram_id(self, value):
        if Profile.objects.filter(telegram_id=value).exists():
            raise ValidationError("!کاربری با این آیدی تلگرام وجود دارد")
        return value


class AdminSingleProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11,
                                         validators=[RegexValidator(regex=r'^09\d{9}$',
                                                                    message="! طول شماره تلفن باید 11 عدد باشد و با 09 شروع شود")])

    class Meta:
        model = Profile
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'email', 'telegram_id']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if value and Profile.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!این نام کاربری برای کاربر دیگری است")
        return value

    def validate_email(self, value):
        if value and Profile.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!کاربری دیگر با این ایمیل وجود دارد")
        return value

    def validate_phone_number(self, value):
        if len(value) != 11:
            raise ValidationError("! شماره تلفن باید متشکل از 11 عدد باشد")

        if not value.startswith('09'):
            raise ValidationError("! شماره تلفن باید با 09 شروع شود")

        if value and Profile.objects.filter(phone_number=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!این شماره تلفن مربوط به یک پروفایل دیگر است")

        return value

    def validate_telegram_id(self, value):
        if value and Profile.objects.filter(telegram_id=value).exclude(id=self.instance.id).exists():
            raise ValidationError("!این آیدی برای شخص دیگریست")
        return value

    def create(self, validated_data):
        passwrod = validated_data.pop('password')
        user = Profile(**validated_data)
        user.set_password(passwrod)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
