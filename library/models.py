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
