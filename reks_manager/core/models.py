import shortuuid
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()

STATUS_CHOICES = [
    ("FOR_ADOPTION", "For Adoption"),
    ("ADOPTED", "Adopted"),
    ("QUARANTINE", "Quarantine"),
    ("UNADOPTABLE", "Unadoptable"),
]

GENDER_CHOICES = [
    ("MALE", "Male"),
    ("FEMALE", "Female"),
]

TYPE_CHOICES = [
    ("DOG", "Dog"),
    ("CAT", "Cat"),
]

RESIDENCE_CHOICES = [("BASE", "Base"), ("TEMPORARY_HOME", "Temporary home")]

""" Gdzie to ma mieć dokładnie zastosowanie? """
ALLERGY_CATEGORY = [
    ("FOOD", "Food"),
    ("CONTACT", "Contact"),
    ("INHALATION", "Inhalation"),
]

DOCTOR_CHOICES = [
    ("PIOTR", "Piotr"),
    ("JOANNA", "Joanna"),
    ("ALEKSANDRA", "Aleksandra"),
]


class Adopter(models.Model):
    id = models.UUIDField(primary_key=True, default=shortuuid.uuid, unique=True)

    owner = models.CharField(max_length=255, verbose_name=_("Full name of owner"))

    phone_number = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(limit_value=9, message=_("Phone number must have 9 digits."))],
        verbose_name=_("Phone number"),
    )
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update date"))

    class Meta:
        verbose_name = _("Adopter")
        verbose_name_plural = _("Adopters")


class TemporaryHome(models.Model):
    id = models.UUIDField(primary_key=True, default=shortuuid.uuid, unique=True)

    owner = models.CharField(max_length=255, verbose_name=_("Full name of owner"))

    phone_number = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(limit_value=9, message=_("Phone number must have 9 digits."))],
        verbose_name=_("Phone number"),
    )

    city = models.CharField(max_length=255, verbose_name=_("City"))
    street = models.CharField(max_length=255, verbose_name=_("Street"))
    building = models.CharField(max_length=20, verbose_name=_("Building number"))
    aparment = models.CharField(max_length=10, verbose_name=_("Apartment number"))

    zip_code = models.CharField(
        max_length=5,
        validators=[MinLengthValidator(limit_value=5, message=_("Zip code must have 5 digits."))],
        verbose_name=_("Phone number"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update date"))

    class Meta:
        verbose_name = _("Temporary home")
        verbose_name_plural = _("Temporary homes")


class Animal(models.Model):
    id = models.UUIDField(primary_key=True, default=shortuuid.uuid, unique=True)
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(limit_value=2, message=_("Name must be at least 2 characters long."))],
    )
    slug = AutoSlugField(populate_from="name", unique=True, auto_created=True, always_update=True)

    animal_type = models.CharField(max_length=255, choices=TYPE_CHOICES, verbose_name=_("Type"))
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name=_("Gender"))

    birth_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="UNADOPTABLE", verbose_name=_("Status"))

    location_where_found = models.CharField(max_length=255)
    date_when_found = models.DateField()

    residence = models.CharField(max_length=255, choices=RESIDENCE_CHOICES, default="BASE")
    description_of_health = models.TextField(blank=True)

    image = models.ImageField(upload_to="animals/")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update date"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animals")
    home = models.ForeignKey(TemporaryHome, on_delete=models.CASCADE, related_name="animals", blank=True)

    def __str__(self):
        return f"{self.animal_type} {self.name}"

    def clean(self):
        super().clean()
        if self.date_when_found < self.birth_date:
            raise ValidationError(_("Date when found cannot be before the birth date."))

    class Meta:
        verbose_name = _("Animal")
        verbose_name_plural = _("Animals")


class HealthCard(models.Model):
    id = models.UUIDField(primary_key=True, default=shortuuid.uuid, unique=True)
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE, related_name="healthcards")

    allergies = models.JSONField()
    drugs = models.JSONField()
    vaccinations = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update date"))

    def __str__(self):
        return f"Health Card of {self.animal.name}"

    class Meta:
        verbose_name = _("Health card")
        verbose_name_plural = _("Health cards")


class VeterinaryVisit(models.Model):
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE, related_name="veterinaryvisits")
    doctor = models.CharField(max_length=255, choices=DOCTOR_CHOICES, verbose_name=_("Doctor"))
    date = models.DateField(verbose_name=_("Date of visit"))
    description = models.TextField(verbose_name=_("Visit description"))

    def __str__(self):
        return f"Visit for {self.health_card.animal.name} by {self.doctor}"

    class Meta:
        verbose_name = _("Veterinary visit")
        verbose_name_plural = _("Veterinary visits")
