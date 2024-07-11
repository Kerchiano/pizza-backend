from django.db import models
from unidecode import unidecode
from django.utils.text import slugify


class SlugMixin(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            def transliterated(data):
                transliterated_data = unidecode(data)
                return slugify(transliterated_data.replace(" ", "-").replace(",", ""))

            if hasattr(self, 'title'):
                self.slug = transliterated(self.title)
            elif hasattr(self, 'address'):
                self.slug = transliterated(self.address)
            elif hasattr(self, 'name'):
                self.slug = transliterated(self.name)
            else:
                raise NotImplementedError('Missing field for slug generation')

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.slug)
