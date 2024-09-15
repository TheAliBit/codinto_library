from django.db import models
from django.utils import timezone

from core.models import BaseModel
from core.models import Profile


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="عنوان دسته‌بندی")
    image = models.ImageField(upload_to='uploads/', verbose_name="تصویر دسته‌بندی")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='children',
                               verbose_name="دسته‌بندی پدر")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.title


class Book(BaseModel, models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان کتاب")
    image = models.ImageField(upload_to='uploads/', verbose_name='عکس')
    author = models.CharField(max_length=255, verbose_name="نویسنده")
    translator = models.CharField(max_length=255, blank=True, null=True, verbose_name="مترجم")
    publisher = models.CharField(max_length=255, verbose_name="انتشارات")
    volume_number = models.PositiveIntegerField(verbose_name="شماره جلد")
    publication_year = models.PositiveIntegerField(
        verbose_name="سال انتشار")  # Changed field name to be more descriptive
    page_count = models.PositiveIntegerField(verbose_name="تعداد صفحه")
    owner = models.CharField(max_length=255, verbose_name="صاحب کتاب")
    description = models.TextField(verbose_name="توضیحات")
    count = models.PositiveIntegerField(verbose_name="تعداد موجودی")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name="books",
                                 verbose_name="دسته‌بندی")

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"

    def __str__(self):
        return self.title


class Review(BaseModel, models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="reviews",
                             verbose_name="کاربر")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name="reviews", verbose_name="کتاب")
    score = models.IntegerField(verbose_name="امتیاز")
    description = models.TextField(verbose_name="متن نظر")

    STATE_CHOICES = [
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='pending', verbose_name="وضعیت")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.user} - {self.book} ({self.score})"


class Notification(BaseModel, models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="notifications",
                             verbose_name="کاربر")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name="notifications",
                             verbose_name="کتاب")
    title = models.CharField(max_length=255, verbose_name="عنوان اطلاع‌رسانی")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='uploads/', verbose_name="تصویر اطلاع‌رسانی")

    TYPE_CHOICES = [
        ('public', 'no sms'),
        ('request', 'sms'),
        ('availabel', 'sms'),
    ]
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default='no_sms', verbose_name="نوع اطلاع‌رسانی")

    class Meta:
        verbose_name = "اطلاع‌رسانی"
        verbose_name_plural = "اطلاع‌رسانی‌ها"

    def __str__(self):
        return self.title


class BaseRequestModel(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="کاربر")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name="کتاب", related_name='requests')

    STATUS_CHOICES = [
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    duration = models.IntegerField(null=True, blank=True, verbose_name="مدت زمان (روز)")

    REQUEST_TYPE_CHOICES = [
        ('borrow', 'Borrow'),
        ('extension', 'Extension'),
        ('return', 'Return'),
        ('review', 'Review'),
    ]
    type = models.CharField(max_length=12, choices=REQUEST_TYPE_CHOICES, default='borrow', verbose_name="نوع درخواست")

    def __str__(self):
        return self.user.username


class BorrowRequest(BaseRequestModel):
    TIME_CHOICES = [
        (14, '14 Days'),
        (30, '30 Days'),
    ]
    time = models.IntegerField(choices=TIME_CHOICES, verbose_name="مدت زمان امانت")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ شروع امانت')

    class Meta:
        verbose_name = "درخواست امانت"
        verbose_name_plural = "درخواست‌های امانت"

    def calculate_duration(self, request):
        self.duration = self.time
        self.start_date = timezone.now()
        self.save(update_fields=['start_date', 'duration'])

    def reset_duration(self):
        self.duration = 0
        self.save()


class ExtensionRequest(BaseRequestModel):
    TIME_CHOICES = [
        (3, '3 Days'),
        (5, '5 Days'),
        (7, '7 Days'),
    ]
    time = models.IntegerField(choices=TIME_CHOICES, verbose_name="مدت زمان تمدید")

    class Meta:
        verbose_name = "درخواست تمدید"
        verbose_name_plural = "درخواست‌های تمدید"

    def extend_duration(self, request):
        self.duration = self.time
        self.save()

    def reset_duration(self):
        self.duration = 0
        self.save()


class ReviewRequest(BaseRequestModel):
    text = models.TextField(max_length=1000, null=True)

    class Meta:
        verbose_name = "درخواست بررسی"
        verbose_name_plural = "درخواست‌های بررسی"


class ReturnRequest(BaseRequestModel):
    class Meta:
        verbose_name = "درخواست بازگشت"
        verbose_name_plural = "درخواست‌های بازگشت"


class History(BaseModel, models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name="کاربر")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name="کتاب")
    request = models.ForeignKey('BaseRequestModel', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="درخواست")

    class Meta:
        verbose_name = "تاریخچه"
        verbose_name_plural = "تاریخچه‌ها"
