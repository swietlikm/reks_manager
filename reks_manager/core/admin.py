from django.contrib import admin
from reks_manager.core.models import Adopter, Animal, TemporaryHome, HealthCard, VeterinaryVisit # noqa


@admin.register(Adopter)
class AdopterAdmin(admin.ModelAdmin):
    list_display = ('owner', 'phone_number', 'address')
    list_filter = ('owner', 'created_at', 'updated_at')
    search_fields = ('owner',)
    readonly_fields = ('id',)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        'animal_type',
        'name',
        'status',
        'residence',
        'user',
        'created_at',
        'updated_at',
    )
    list_filter = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('id',)


@admin.register(TemporaryHome)
class TemporaryHomeAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'phone_number',
        'city',
        'street',
        'building',
        'apartment',
    )
    list_filter = ('owner', 'city', 'street', 'created_at', 'updated_at')
    search_fields = ('owner',)
    readonly_fields = ('id',)


@admin.register(HealthCard)
class HealthCardAdmin(admin.ModelAdmin):
    list_display = (
        'animal',
        'created_at',
        'updated_at',
    )
    list_filter = ('animal', 'created_at', 'updated_at')
    search_fields = ('animal',)
    readonly_fields = ('id',)


@admin.register(VeterinaryVisit)
class VeterinaryVisitAdmin(admin.ModelAdmin):
    list_display = (
        'health_card',
        'doctor',
        'date',
        'created_at',
        'updated_at',
    )
    list_filter = ('health_card', 'doctor', 'date', 'created_at', 'updated_at')
    search_fields = ('health_card.animal.name', 'doctor')
    readonly_fields = ('id',)
