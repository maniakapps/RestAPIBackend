import datetime

from django.db import models


class Company(models.Model):
    """ A class that models a company"""
    name = models.CharField("The name of company", max_length=200)
    website = models.URLField("The website of the company", max_length=200, default="", blank=True)
    foundation = models.IntegerField("The year of foundation")
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        """Returns a string representation of the company"""
        return f"{self.name}"
