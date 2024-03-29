# Generated by Django 4.2.7 on 2023-11-08 18:30

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_alter_animal_id_alter_healthcard_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adopter",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="abcdefg1234",
                length=16,
                max_length=40,
                prefix="a_",
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="12345", length=6, max_length=6, prefix="p_", primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="healthcard",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="12345", length=7, max_length=7, prefix="hc_", primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="temporaryhome",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="abcdefg1234", length=16, max_length=40, prefix="th_", primary_key=True, serialize=False
            ),
        ),
    ]
