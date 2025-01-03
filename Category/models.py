from django.db import models


class CaseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی پرونده")
    description = models.TextField(verbose_name="توضیحات دسته‌بندی پرونده", blank=True, null=True)

    def __str__(self):
        return self.name
