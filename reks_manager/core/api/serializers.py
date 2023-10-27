from rest_framework import serializers

from reks_manager.core.models import Animal, HealthCard, Allergy, Medication, Vaccination, VeterinaryVisit
from reks_manager.users.api.serializers import UserSerializer


class AllergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = "__all__"


class MedicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = "__all__"


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = "__all__"


class VeterinaryVisitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryVisit
        fields = "__all__"


class HealthCardSerializer(serializers.ModelSerializer):
    allergies = AllergiesSerializer(many=True, read_only=True)
    medications = MedicationsSerializer(many=True, read_only=True)
    vaccinations = VaccinationSerializer(many=True, read_only=True)
    veterinary_visits = VeterinaryVisitsSerializer(many=True, read_only=True, source='veterinaryvisits')

    class Meta:
        model = HealthCard
        fields = "__all__"


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


