# Generated by Django 4.2.6 on 2023-11-03 13:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_remove_user_name_user_first_name_user_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                max_length=255,
                validators=[
                    django.core.validators.MinLengthValidator(
                        limit_value=2, message="Name must be at least 2 characters long."
                    )
                ],
                verbose_name="First name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                max_length=255,
                validators=[
                    django.core.validators.MinLengthValidator(
                        limit_value=2, message="Name must be at least 2 characters long."
                    )
                ],
                verbose_name="Last name",
            ),
        ),
    ]
