from shortuuid.django_fields import ShortUUIDField
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()

STATUS_CHOICES = [
    ("DO_ADOPCJI", _("For Adoption")),
    ("ZAADOPTOWANY", _("Zaadoptowany")),
    ("KWARANTANNA", _("Kwarantanna")),
    ("NIE_DO_ADOPCJI", _("Nie do adopcji")),
]

GENDER_CHOICES = [
    ("SAMIEC", _("Samiec")),
    ("SAMICA", _("Samica")),
]

TYPE_CHOICES = [
    ("PIES", _("Pies")),
    ("KOT", _("Kot")),
]

RESIDENCE_CHOICES = [("SCHRONISKO", _("Schronisko")), ("TYMCZASOWY_DOM", _("Tymczasowy dom"))]

""" Gdzie to ma mieć dokładnie zastosowanie? """
ALLERGY_CATEGORY = [
    ("POKARM", _("Pokarm")),
    ("KONTAKT", _("Kontakt")),
    ("INHALACJA", _("Inhalacja")),
]

DOCTOR_CHOICES = [
    ("PIOTR", "Piotr"),
    ("JOANNA", "Joanna"),
    ("ALEKSANDRA", "Aleksandra"),
]


class Allergy(models.Model):
    category = models.CharField(max_length=255, choices=ALLERGY_CATEGORY, verbose_name=_("Allergy category"))
    name = models.CharField(max_length=255, verbose_name=_("Allergy name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return _("Allergy") + f": {self.category} {self.name}"

    class Meta:
        verbose_name = _("Allergy")
        verbose_name_plural = _("Allergies")


class Medication(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Medication name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return _("Medication") + f": {self.name}"

    class Meta:
        verbose_name = _("Medication")
        verbose_name_plural = _("Medications")


class Vaccination(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Vaccination name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return _("Vaccination") + f": {self.name}"

    class Meta:
        verbose_name = _("Vaccination")
        verbose_name_plural = _("Vaccinations")


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
        return f'{_("Adopter")} {self.owner}'

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
        verbose_name=_("Name"),
    )
    slug = AutoSlugField(populate_from="name", unique=True, auto_created=True, always_update=True)

    animal_type = models.CharField(max_length=255, choices=TYPE_CHOICES, verbose_name=_("Type"))
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name=_("Gender"))

    birth_date = models.DateField(verbose_name=_("Birth date"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="NIE_DO_ADOPCJI", verbose_name=_("Status"))

    location_where_found = models.CharField(blank=True, max_length=255, verbose_name=_("Location where found"))
    date_when_found = models.DateField(blank=True, null=True, verbose_name=_("Date when found"))

    residence = models.CharField(
        max_length=255, choices=RESIDENCE_CHOICES, default="SCHRONISKO", verbose_name=_("Residence")
    )
    description_of_health = models.TextField(blank=True, verbose_name=_("Health description"))

    image = models.ImageField(blank=True, null=True, upload_to="animals/", verbose_name=_("Photo"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animals", verbose_name=_("Added by"))
    adopted_by = models.ForeignKey(
        Adopter,
        on_delete=models.CASCADE,
        related_name='animals',
        verbose_name=_('Adopted by'),
        blank=True,
        null=True)

    home = models.ForeignKey(
        TemporaryHome, on_delete=models.CASCADE, related_name="animals", blank=True, null=True, verbose_name=_("Home")
    )

    def __str__(self):
        return f"{_(self.animal_type)} {self.name}"

    def clean(self):
        super().clean()
        if self.date_when_found < self.birth_date:
            raise ValidationError(_("Date when found cannot be before the birth date."))

    def adopt(self, adopter):
        self.adopted_by = adopter
        self.status = "ZAADOPTOWANY"
        self.save()

    def remove_adopter(self):
        self.adopted_by = None
        self.status = "DO_ADOPCJI"
        self.save()

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
    animal = models.OneToOneField(
        Animal, on_delete=models.CASCADE, related_name="healthcards", verbose_name=_("Animal")
    )

    allergies = models.ManyToManyField(Allergy, through="HealthCardAllergy", blank=True, verbose_name=_("Allergies"))
    medications = models.ManyToManyField(
        Medication, through="HealthCardMedication", blank=True, verbose_name=_("Medications")
    )
    vaccinations = models.ManyToManyField(
        Vaccination, through="HealthCardVaccination", blank=True, verbose_name=_("Vaccinations")
    )

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


class HealthCardAllergy(models.Model):
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE, verbose_name=_("Health card"), related_name='healthcardallergies')
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE, verbose_name=_("Allergy"))
    description = models.TextField(max_length=255, blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.health_card} - Allergy: {self.allergy}"

    class Meta:
        verbose_name = _("Health card - Allergy")
        verbose_name_plural = _("Health card - Allergies")


class HealthCardMedication(models.Model):
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE, verbose_name=_("Health card"), related_name='healthcardmedications')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, verbose_name=_("Medication"))
    description = models.TextField(max_length=255, blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.health_card} - Medication: {self.medication}"

    class Meta:
        verbose_name = _("Health card - Medication")
        verbose_name_plural = _("Health card - Medications")


class HealthCardVaccination(models.Model):
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE, verbose_name=_("Health card"), related_name='healthcardvaccinations')
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE, verbose_name=_("Vaccination"))
    vaccination_date = models.DateField(verbose_name=_("Vaccination date"))
    description = models.TextField(max_length=255, blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.health_card} - Vaccination: {self.vaccination}"

    class Meta:
        verbose_name = _("Health card - Vaccination")
        verbose_name_plural = _("Health card - Vaccinations")
