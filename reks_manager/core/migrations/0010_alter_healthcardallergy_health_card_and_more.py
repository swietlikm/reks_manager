# Generated by Django 4.2.6 on 2023-11-03 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_alter_animal_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthcardallergy",
            name="health_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="healthcardallergies",
                to="core.healthcard",
                verbose_name="Karta zdrowia",
            ),
        ),
        migrations.AlterField(
            model_name="healthcardmedication",
            name="health_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="healthcardmedications",
                to="core.healthcard",
                verbose_name="Karta zdrowia",
            ),
        ),
        migrations.AlterField(
            model_name="healthcardvaccination",
            name="health_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="healthcardvaccinations",
                to="core.healthcard",
                verbose_name="Karta zdrowia",
            ),
        ),
    ]
