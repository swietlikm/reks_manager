# Generated by Django 4.2.6 on 2023-10-29 08:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(default="Mateusz", max_length=255, verbose_name="First name"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(default="Mateusz", max_length=255, verbose_name="Last name"),
            preserve_default=False,
        ),
    ]
