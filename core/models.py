from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Profile(AbstractUser):
    username = models.CharField(max_length=255, unique=True, verbose_name="نام کاربری")
    password = models.CharField(max_length=255, verbose_name="رمزعبور")
    first_name = models.CharField(max_length=255, verbose_name="نام")
    last_name = models.CharField(max_length=255, verbose_name="نام خانوادگی")
    phone_number = models.CharField(max_length=255, verbose_name="شماره تلفن")
    email = models.EmailField(max_length=255, verbose_name="ایمیل")
    telegram_id = models.CharField(max_length=255, verbose_name="آیدی تلگرام")
    picture = models.ImageField(upload_to='uploads/', verbose_name='آواتار')

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"


class TimeStampedAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
