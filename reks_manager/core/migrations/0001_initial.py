import autoslug.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Adopter",
            fields=[
                (
                    "id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefg1234", length=16, max_length=40, prefix="", primary_key=True, serialize=False
                    ),
                ),
                ("owner", models.CharField(max_length=255, verbose_name="Full name of owner")),
                (
                    "phone_number",
                    models.CharField(
                        max_length=9,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=9, message="Phone number must have 9 digits."
                            )
                        ],
                        verbose_name="Phone number",
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=255, verbose_name="Address")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated at")),
            ],
            options={
                "verbose_name": "Adopter",
                "verbose_name_plural": "Adopters",
            },
        ),
        migrations.CreateModel(
            name="Animal",
            fields=[
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        always_update=True, auto_created=True, editable=False, populate_from="name", unique=True
                    ),
                ),
                (
                    "id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefg1234", length=16, max_length=40, prefix="", primary_key=True, serialize=False
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2, message="Name must be at least 2 characters long."
                            )
                        ],
                    ),
                ),
                (
                    "animal_type",
                    models.CharField(choices=[("DOG", "Dog"), ("CAT", "Cat")], max_length=255, verbose_name="Typ"),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("MALE", "Male"), ("FEMALE", "Female")], max_length=50, verbose_name="Gender"
                    ),
                ),
                ("birth_date", models.DateField(verbose_name="Birth date")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("FOR_ADOPTION", "For Adoption"),
                            ("ADOPTED", "Adopted"),
                            ("QUARANTINE", "Quarantine"),
                            ("UNADOPTABLE", "Unadoptable"),
                        ],
                        default="UNADOPTABLE",
                        max_length=255,
                        verbose_name="Status",
                    ),
                ),
                ("location_where_found", models.CharField(max_length=255, verbose_name="Location where found")),
                ("date_when_found", models.DateField(verbose_name="Date when found")),
                (
                    "residence",
                    models.CharField(
                        choices=[("BASE", "Base"), ("TEMPORARY_HOME", "Temporary home")],
                        default="BASE",
                        max_length=255,
                    ),
                ),
                ("description_of_health", models.TextField(blank=True, verbose_name="Health description")),
                ("image", models.ImageField(upload_to="animals/", verbose_name="Photo")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated at")),
            ],
            options={
                "verbose_name": "Animal",
                "verbose_name_plural": "Animals",
            },
        ),
        migrations.CreateModel(
            name="HealthCard",
            fields=[
                (
                    "id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefg1234", length=16, max_length=40, prefix="", primary_key=True, serialize=False
                    ),
                ),
                ("allergies", models.JSONField()),
                ("drugs", models.JSONField()),
                ("vaccinations", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated at")),
                (
                    "animal",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="healthcards", to="core.animal"
                    ),
                ),
            ],
            options={
                "verbose_name": "Health card",
                "verbose_name_plural": "Health cards",
            },
        ),
        migrations.CreateModel(
            name="TemporaryHome",
            fields=[
                (
                    "id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefg1234", length=16, max_length=40, prefix="", primary_key=True, serialize=False
                    ),
                ),
                ("owner", models.CharField(max_length=255, verbose_name="Full name of owner")),
                (
                    "phone_number",
                    models.CharField(
                        max_length=9,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=9, message="Phone number must have 9 digits."
                            )
                        ],
                        verbose_name="Phone number",
                    ),
                ),
                ("city", models.CharField(max_length=255, verbose_name="City")),
                ("street", models.CharField(max_length=255, verbose_name="Street")),
                ("building", models.CharField(max_length=20, verbose_name="Building number")),
                ("apartment", models.CharField(blank=True, max_length=10, verbose_name="Apartment number")),
                (
                    "zip_code",
                    models.CharField(
                        max_length=5,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=5, message="Zip code must have 5 digits."
                            )
                        ],
                        verbose_name="Zip code",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Creation date")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Update date")),
            ],
            options={
                "verbose_name": "Temporary home",
                "verbose_name_plural": "Temporary homes",
            },
        ),
        migrations.CreateModel(
            name="VeterinaryVisit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "doctor",
                    models.CharField(
                        choices=[("PIOTR", "Piotr"), ("JOANNA", "Joanna"), ("ALEKSANDRA", "Aleksandra")],
                        max_length=255,
                        verbose_name="Doctor",
                    ),
                ),
                ("date", models.DateField(verbose_name="Date of visit")),
                ("description", models.TextField(verbose_name="Visit description")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated at")),
                (
                    "health_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="veterinaryvisits",
                        to="core.healthcard",
                    ),
                ),
            ],
            options={
                "verbose_name": "Veterinary visit",
                "verbose_name_plural": "Veterinary visits",
            },
        ),
        migrations.AddField(
            model_name="animal",
            name="home",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="animals",
                to="core.temporaryhome",
            ),
        ),
        migrations.AddField(
            model_name="animal",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="animals", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
