# Generated by Django 4.2.7 on 2023-11-08 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0011_animal_adopted_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="adopter",
            name="owner",
        ),
        migrations.AddField(
            model_name="adopter",
            name="name",
            field=models.CharField(default="Mateusz", max_length=255, verbose_name="Full name of adopter"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="animal",
            name="added_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="animals",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Added by",
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="abcdefg1234", length=6, max_length=8, prefix="", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="healthcard",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="abcdefg1234", length=6, max_length=8, prefix="", primary_key=True, serialize=False
            ),
        ),
    ]
