# Generated by Django 5.1 on 2024-12-02 06:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("payments", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChapaTransaction",
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
                ("pay_url", models.URLField()),
                ("charge_price", models.FloatField(default=0)),
                ("amount", models.BigIntegerField(default=0)),
                ("is_paid", models.BooleanField(default=False)),
                (
                    "reference_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("tx_ref", models.CharField(max_length=500)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]