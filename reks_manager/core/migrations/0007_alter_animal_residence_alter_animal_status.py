# Generated by Django 4.2.6 on 2023-10-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_alter_allergy_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="residence",
            field=models.CharField(
                choices=[("SCHRONISKO", "Schronisko"), ("TYMCZASOWY_DOM", "Tymczasowy dom")],
                default="SCHRONISKO",
                max_length=255,
                verbose_name="Miejsce przebywania",
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="status",
            field=models.CharField(
                choices=[
                    ("DO_ADOPCJI", "Do adopcji"),
                    ("ZAADOPTOWANY", "Zaadoptowany"),
                    ("KWARANTANNA", "Kwarantanna"),
                    ("NIEADOPTOWALNY", "Nieadoptowalny"),
                ],
                default="NIEADOPTOWALNY",
                max_length=255,
                verbose_name="Status",
            ),
        ),
    ]
