from django.db import models
from core.models import TimeStampedAbstractModel


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="عنوان دسته بندی")
    image = models.ImageField(upload_to='uploads/', verbose_name="تصویر دسته بندی")
    parent = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='children',
                               verbose_name="دسته بندی پدر")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Book(TimeStampedAbstractModel, models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان کتاب")
    author = models.CharField(max_length=255, verbose_name="نویسنده")
    translator = models.CharField(max_length=255, blank=True, null=True, verbose_name="مترجم")
    publisher = models.CharField(max_length=255, verbose_name="انتشارات")
    volume_number = models.IntegerField(verbose_name="شماره جلد")
    publication_count = models.IntegerField(verbose_name="سال انتشار")
    page_count = models.IntegerField(verbose_name="تعداد صفحه")
    owner = models.CharField(max_length=255, verbose_name="صاحب کتاب")
    description = models.TextField(verbose_name="توضیحات")
    count = models.IntegerField(verbose_name="تعداد موجودی")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name="books", verbose_name="دسته بندی")

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب ها"
