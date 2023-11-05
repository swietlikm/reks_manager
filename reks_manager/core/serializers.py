from django.utils import timezone
from rest_framework import serializers

from .models import Animal, HealthCard, Allergy, Medication, Vaccination, VeterinaryVisit, HealthCardVaccination, HealthCardMedication, HealthCardAllergy, TemporaryHome, Adopter
from reks_manager.users.api.serializers import UserSerializer


class AllergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'


class MedicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'


class VaccinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = '__all__'

    def validate_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Date of vaccination cannot be in the future.")
        return value


class VeterinaryVisitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryVisit
        fields = '__all__'

    def validate_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Date of visit cannot be in the future.")
        return value


class TemporaryHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryHome
        fields = '__all__'


class AdopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = '__all__'


class HealthCardAllergySerializer(serializers.ModelSerializer):
    allergy = AllergiesSerializer()

    class Meta:
        model = HealthCardAllergy
        fields = ['allergy', 'description']


class HealthCardMedicationSerializer(serializers.ModelSerializer):
    medication = MedicationsSerializer()

    class Meta:
        model = HealthCardMedication
        fields = ['medication', 'description']


class HealthCardVaccinationSerializer(serializers.ModelSerializer):
    vaccination = VaccinationsSerializer()

    class Meta:
        model = HealthCardVaccination
        fields = ['vaccination', 'vaccination_date', 'description']


class HealthCardSerializer(serializers.ModelSerializer):
    allergies = HealthCardAllergySerializer(many=True, source='healthcardallergies', required=False)
    medications = HealthCardMedicationSerializer(many=True, source='healthcardmedications', required=False)
    vaccinations = HealthCardVaccinationSerializer(many=True, source='healthcardvaccinations', required=False)
    veterinary_visits = VeterinaryVisitsSerializer(many=True, source='veterinaryvisits', required=False)

    class Meta:
        model = HealthCard
        fields = '__all__'

    def create(self, validated_data):
        # Create HealthCard object
        allergies_data = validated_data.pop('allergies', [])
        medications_data = validated_data.pop('medications', [])
        vaccinations_data = validated_data.pop('vaccinations', [])

        health_card = HealthCard.objects.create(**validated_data)

        # Create related objects and associate them with the HealthCard
        for allergy_data in allergies_data:
            HealthCardAllergy.objects.create(health_card=health_card, **allergy_data)

        for medication_data in medications_data:
            HealthCardMedication.objects.create(health_card=health_card, **medication_data)

        for vaccination_data in vaccinations_data:
            HealthCardVaccination.objects.create(health_card=health_card, **vaccination_data)

        return health_card


class AnimalSerializer(serializers.ModelSerializer):
    added_by = UserSerializer()
    health_card = HealthCardSerializer(source="healthcards")

    class Meta:
        model = Animal
        fields = [
            "id",
            "name",
            "slug",
            "animal_type",
            "gender",
            "birth_date",
            "description",
            "status",
            "location_where_found",
            "date_when_found",
            "description_of_health",
            "residence",
            "image",

            "home",
            "added_by",

            "health_card",

            "created_at",
            "updated_at",
        ]

#  ------------------------------------------------------------
#  PUBLIC
#  ------------------------------------------------------------


class AnimalPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = [
            "name",
            "slug",
            "animal_type",
            "gender",
            "birth_date",
            "description",
            "status",
            "description_of_health",
            "residence",
            "image",

            "created_at",
        ]
