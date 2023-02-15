from django.core.validators import URLValidator, MaxValueValidator
from django.db import models
from django.db.models import CharField
from django.utils import timezone
import uuid


class Company(models.Model):
    """A class that models a company"""

    name = models.CharField("The name of company", max_length=200, unique=True)
    website = models.URLField("The website of the company", max_length=200, default="", blank=True, validators=[URLValidator()])
    foundation = models.DateField("The date of foundation", validators=[MaxValueValidator(timezone.now().date())])
    description = models.TextField("A brief description of the company", blank=True)
    logo = models.ImageField("The company logo", upload_to='logos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    identifier = models.CharField("The unique identifier of the company", max_length=50, unique=True)

    def save(self, *args, **kwargs):
        """Override the default save method to set the identifier"""
        if not self.identifier:
            self.identifier = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self) -> CharField:
        """Returns a string representation of the company"""
        return self.name

    class Meta:
        ordering = ['name']
