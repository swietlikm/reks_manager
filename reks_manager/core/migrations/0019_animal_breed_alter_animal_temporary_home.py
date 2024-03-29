# Generated by Django 4.2.7 on 2023-11-12 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0018_remove_animal_home_animal_temporary_home_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="animal",
            name="breed",
            field=models.CharField(
                blank=True, choices=[("SAMIEC", "Samiec"), ("SAMICA", "Samica")], max_length=255, verbose_name="Bread"
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="temporary_home",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="animals",
                to="core.temporaryhome",
                verbose_name="Dom tymczasowy",
            ),
        ),
    ]
