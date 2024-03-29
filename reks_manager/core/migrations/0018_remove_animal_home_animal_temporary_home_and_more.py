# Generated by Django 4.2.7 on 2023-11-12 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0017_alter_healthcard_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="animal",
            name="home",
        ),
        migrations.AddField(
            model_name="animal",
            name="temporary_home",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="animals",
                to="core.temporaryhome",
                verbose_name="Dom tymczasowy",
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="added_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="animals",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Dodany przez",
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="adopted_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="animals",
                to="core.adopter",
                verbose_name="Adopted by",
            ),
        ),
        migrations.AlterField(
            model_name="medication",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="Medication name"),
        ),
        migrations.AlterField(
            model_name="vaccination",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="Nazwa szczepionki"),
        ),
        migrations.AlterUniqueTogether(
            name="adopter",
            unique_together={("name", "phone_number", "address")},
        ),
        migrations.AlterUniqueTogether(
            name="allergy",
            unique_together={("category", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="temporaryhome",
            unique_together={("owner", "phone_number")},
        ),
    ]
