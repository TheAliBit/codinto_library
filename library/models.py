from django.db import models
from core.models import TimeStampedAbstractModel
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


class Book(TimeStampedAbstractModel):
    title = models.CharField(max_length=255, verbose_name="عنوان کتاب")
    author = models.CharField(max_length=255, verbose_name="نویسنده")
    translator = models.CharField(max_length=255, blank=True, null=True, verbose_name="مترجم")
    publisher = models.CharField(max_length=255, verbose_name="انتشارات")
    volume_number = models.IntegerField(verbose_name="شماره جلد")
    publication_year = models.IntegerField(verbose_name="سال انتشار")  # Changed field name to be more descriptive
    page_count = models.IntegerField(verbose_name="تعداد صفحه")
    owner = models.CharField(max_length=255, verbose_name="صاحب کتاب")
    description = models.TextField(verbose_name="توضیحات")
    count = models.IntegerField(verbose_name="تعداد موجودی")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name="books",
                                 verbose_name="دسته‌بندی")

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"

    def __str__(self):
        return self.title


class Review(TimeStampedAbstractModel):
    user = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, related_name="reviews",
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
