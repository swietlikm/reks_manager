from shortuuid.django_fields import ShortUUIDField
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()

STATUS_CHOICES = [
    ("FOR_ADOPTION", _("For Adoption")),
    ("ADOPTED", _("Adopted")),
    ("QUARANTINE", _("Quarantine")),
    ("UNADOPTABLE", _("Unadoptable")),
]

GENDER_CHOICES = [
    ("MALE", _("Male")),
    ("FEMALE", _("Female")),
]

TYPE_CHOICES = [
    ("DOG", _("Dog")),
    ("CAT", _("Cat")),
]

RESIDENCE_CHOICES = [
    ("BASE", _("Base")),
    ("TEMPORARY_HOME", _("Temporary home"))]

""" Gdzie to ma mieć dokładnie zastosowanie? """
ALLERGY_CATEGORY = [
    ("FOOD", _("Food")),
    ("CONTACT", _("Contact")),
    ("INHALATION", _("Inhalation")),
]

DOCTOR_CHOICES = [
    ("PIOTR", "Piotr"),
    ("JOANNA", "Joanna"),
    ("ALEKSANDRA", "Aleksandra"),
]


class Adopter(models.Model):
    id = ShortUUIDField(
        primary_key=True,
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
    )

    owner = models.CharField(max_length=255, verbose_name=_("Full name of owner"))

    phone_number = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(limit_value=9, message=_("Phone number must have 9 digits."))],
        verbose_name=_("Phone number"),
    )
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return f'Adopter {self.owner}'

    class Meta:
        verbose_name = _("Adopter")
        verbose_name_plural = _("Adopters")


class TemporaryHome(models.Model):
    id = ShortUUIDField(
        primary_key=True,
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
    )

    owner = models.CharField(max_length=255, verbose_name=_("Full name of owner"))

    phone_number = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(limit_value=9, message=_("Phone number must have 9 digits."))],
        verbose_name=_("Phone number"),
    )

    city = models.CharField(max_length=255, verbose_name=_("City"))
    street = models.CharField(max_length=255, verbose_name=_("Street"))
    building = models.CharField(max_length=20, verbose_name=_("Building number"))
    apartment = models.CharField(blank=True, max_length=10, verbose_name=_("Apartment number"))

    zip_code = models.CharField(
        max_length=5,
        validators=[MinLengthValidator(limit_value=5, message=_("Zip code must have 5 digits."))],
        verbose_name=_("Zip code"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update date"))

    def __str__(self):
        return f'{_("Temporary home")} | {self.owner} | {self.city} | {self.street} {self.building}'

    class Meta:
        verbose_name = _("Temporary home")
        verbose_name_plural = _("Temporary homes")


class Animal(models.Model):
    id = ShortUUIDField(
        primary_key=True,
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
    )
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(limit_value=2, message=_("Name must be at least 2 characters long."))],
        verbose_name=_('Name')
    )
    slug = AutoSlugField(populate_from="name", unique=True, auto_created=True, always_update=True)

    animal_type = models.CharField(max_length=255, choices=TYPE_CHOICES, verbose_name=_("Type"))
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name=_("Gender"))

    birth_date = models.DateField(verbose_name=_('Birth date'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="UNADOPTABLE", verbose_name=_("Status"))

    location_where_found = models.CharField(max_length=255, verbose_name=_('Location where found'))
    date_when_found = models.DateField(verbose_name=_('Date when found'))

    residence = models.CharField(max_length=255, choices=RESIDENCE_CHOICES, default="BASE", verbose_name=_('Residence'))
    description_of_health = models.TextField(blank=True, verbose_name=_('Health description'))

    image = models.ImageField(upload_to="animals/", verbose_name=_('Photo'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="animals",
        verbose_name=_('User'))

    home = models.ForeignKey(
        TemporaryHome,
        on_delete=models.CASCADE,
        related_name="animals",
        blank=True,
        null=True,
        verbose_name=_('Home'))

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
    id = ShortUUIDField(
        primary_key=True,
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
    )
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE, related_name="healthcards")

    allergies = models.JSONField()
    drugs = models.JSONField()
    vaccinations = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return f"{_('Health Card of')} {self.animal.name}"

    class Meta:
        verbose_name = _("Health card")
        verbose_name_plural = _("Health cards")


class VeterinaryVisit(models.Model):
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE, related_name="veterinaryvisits")
    doctor = models.CharField(max_length=255, choices=DOCTOR_CHOICES, verbose_name=_("Doctor"))
    date = models.DateField(verbose_name=_("Date of visit"))
    description = models.TextField(verbose_name=_("Visit description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return f"{_('Visit for')} {self.health_card.animal.name} {_('by')} {self.doctor}"

    class Meta:
        verbose_name = _("Veterinary visit")
        verbose_name_plural = _("Veterinary visits")
