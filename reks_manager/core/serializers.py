from rest_framework import serializers

from .models import Animal, HealthCard, Allergy, Medication, Vaccination, VeterinaryVisit, HealthCardVaccination, HealthCardMedication, HealthCardAllergy, TemporaryHome, Adopter
from reks_manager.users.api.serializers import UserSerializer

from .models import ALLERGY_CATEGORY


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


class VeterinaryVisitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryVisit
        fields = '__all__'


class TemporaryHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryHome
        fields = '__all__'


class AdopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = '__all__'


class HealthCardAllergySerializer(serializers.ModelSerializer):
    allergy = AllergiesSerializer(read_only=True)

    class Meta:
        model = HealthCardAllergy
        fields = ['allergy', 'description']


class HealthCardMedicationSerializer(serializers.ModelSerializer):
    medication = MedicationsSerializer(read_only=True)

    class Meta:
        model = HealthCardMedication
        fields = ['medication', 'description']


class HealthCardVaccinationSerializer(serializers.ModelSerializer):
    vaccination = VaccinationsSerializer(read_only=True)

    class Meta:
        model = HealthCardVaccination
        fields = ['vaccination', 'vaccination_date', 'description']


class HealthCardSerializer(serializers.ModelSerializer):
    allergies = HealthCardAllergySerializer(many=True, read_only=True, source='healthcardallergies')
    medications = HealthCardMedicationSerializer(many=True, read_only=True, source='healthcardmedications')
    vaccinations = HealthCardVaccinationSerializer(many=True, read_only=True, source='healthcardvaccinations')
    veterinary_visits = VeterinaryVisitsSerializer(many=True, read_only=True, source='veterinaryvisits')

    class Meta:
        model = HealthCard
        fields = [
            'allergies',
            'medications',
            'vaccinations',
            'veterinary_visits',
        ]


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
