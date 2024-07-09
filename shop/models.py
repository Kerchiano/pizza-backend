from django.db import models

from pizza_backend import settings

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    title = models.CharField(max_length=100)
    icon = models.FileField(upload_to='category/')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
