# Generated by Django 4.1 on 2022-08-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="The name of comapy"),
                ),
                (
                    "website",
                    models.URLField(
                        blank=True,
                        default="",
                        verbose_name="The website of the company",
                    ),
                ),
                (
                    "foundation",
                    models.IntegerField(verbose_name="The year of foundation"),
                ),
            ],
        ),
    ]
