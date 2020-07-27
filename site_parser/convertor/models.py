from django.core.validators import URLValidator, FileExtensionValidator
from django.db import models
from django.core.exceptions import ValidationError


class ConvertorData(models.Model):
    email = models.EmailField(null=True, blank=True)
    source = models.TextField()
    output = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    is_url = models.BooleanField(default=False)
    domain = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            URLValidator()(self.source)
            is_url = True
        except ValidationError:
            is_url = False
        self.is_url = is_url
        return super(ConvertorData, self).save(*args, **kwargs)