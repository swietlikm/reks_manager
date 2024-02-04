from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (
    Adopter,
    Allergy,
    Animal,
    HealthCard,
    HealthCardAllergy,
    HealthCardMedication,
    HealthCardVaccination,
    Medication,
    TemporaryHome,
    Vaccination,
    VeterinaryVisit,
)


@admin.register(Adopter)
class AdopterAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "address", "updated_at")
    list_filter = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("id",)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "animal_type",
        "name",
        "status",
        "residence",
        "created_at",
        "updated_at",
    )
    list_filter = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("slug", "id", "added_by")

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "added_by"):
            if not obj.added_by:
                obj.added_by = request.user
        obj.save()


@admin.register(TemporaryHome)
class TemporaryHomeAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "phone_number",
        "city",
        "street",
        "building",
        "apartment",
    )
    list_filter = ("owner", "city", "street", "created_at", "updated_at")
    search_fields = ("owner",)
    readonly_fields = ("id",)


@admin.register(VeterinaryVisit)
class VeterinaryVisitAdmin(admin.ModelAdmin):
    list_display = (
        "health_card",
        "doctor",
        "date",
        "created_at",
        "updated_at",
    )
    list_filter = ("health_card", "doctor", "date", "created_at", "updated_at")
    search_fields = ("health_card.animal.name", "doctor")


class HealthCardAllergyInline(admin.StackedInline):
    model = HealthCardAllergy
    extra = 1  # Number of empty forms to display


class HealthCardMedicationInline(admin.StackedInline):
    model = HealthCardMedication
    extra = 1  # Number of empty forms to display


class HealthCardVaccinationInline(admin.StackedInline):
    model = HealthCardVaccination
    extra = 1  # Number of empty forms to display


@admin.register(HealthCard)
class HealthCardAdmin(admin.ModelAdmin):
    inlines = [HealthCardVaccinationInline, HealthCardAllergyInline, HealthCardMedicationInline]
    list_display = (
        "id",
        "animal",
        "allergies_count",
        "medications_count",
        "vaccinations_count",
        "created_at",
        "updated_at",
    )
    fields = ("animal",)
    readonly_fields = ("id",)
    list_filter = (
        "animal",
        "created_at",
        "updated_at",
    )

    @admin.display(
        description=_("Allergies Count"),
        ordering="Allergies__Count",
    )
    def allergies_count(self, obj):
        return obj.allergies.count()

    @admin.display(
        description=_("Medications Count"),
        ordering="medications__count",
    )
    def medications_count(self, obj):
        return obj.medications.count()

    @admin.display(
        description=_("Vaccinations Count"),
        ordering="vaccinations__count",
    )
    def vaccinations_count(self, obj):
        return obj.vaccinations.count()


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "name",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "name", "created_at", "updated_at")
    search_fields = ("category", "name")


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    list_filter = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    list_filter = ("name", "created_at", "updated_at")
    search_fields = ("name",)
