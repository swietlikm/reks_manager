# Generated by Django 4.2.6 on 2023-10-25 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_healthcardallergy_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthcardallergy",
            name="allergy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.allergy", verbose_name="Allergy"
            ),
        ),
        migrations.AlterField(
            model_name="healthcardallergy",
            name="health_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.healthcard", verbose_name="Karta zdrowia"
            ),
        ),
        migrations.AlterField(
            model_name="healthcardmedication",
            name="health_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.healthcard", verbose_name="Karta zdrowia"
            ),
        ),
        migrations.AlterField(
            model_name="healthcardmedication",
            name="medication",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.medication", verbose_name="Medication"
            ),
        ),
        migrations.AlterField(
            model_name="healthcardvaccination",
            name="health_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.healthcard", verbose_name="Karta zdrowia"
            ),
        ),
        migrations.AlterField(
            model_name="healthcardvaccination",
            name="vaccination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.vaccination", verbose_name="Vaccination"
            ),
        ),
    ]