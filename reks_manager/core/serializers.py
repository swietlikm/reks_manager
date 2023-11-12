from django.utils import timezone
from django.utils.translation import gettext as _
from reks_manager.users.api.serializers import UserSerializer
from rest_framework import serializers

from .models import Animal, HealthCard, Allergy, Medication, Vaccination, VeterinaryVisit, HealthCardVaccination, \
    HealthCardMedication, HealthCardAllergy, TemporaryHome, Adopter


# SIMPLE #################################

class AllergiesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Allergy
        fields = '__all__'


class MedicationsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Medication
        fields = '__all__'


class VaccinationsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Vaccination
        fields = '__all__'

    def validate_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Date of vaccination cannot be in the future.")
        return value


class VeterinaryVisitsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = VeterinaryVisit
        fields = '__all__'

    def validate_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Date of visit cannot be in the future.")
        return value


class TemporaryHomeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = TemporaryHome
        fields = '__all__'


class AdopterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Adopter
        fields = '__all__'

# INTERMEDIATE #################################


class HealthCardAllergySerializer(serializers.ModelSerializer):
    allergy = AllergiesSerializer(read_only=True)

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


class HealthCardWriteSerializer(serializers.ModelSerializer):
    class HealthCardAllergyWriteSerializer(serializers.ModelSerializer):
        class Meta:
            model = HealthCardAllergy
            fields = ['allergy', 'description']

    class HealthCardMedicationWriteSerializer(serializers.ModelSerializer):

        class Meta:
            model = HealthCardMedication
            fields = ['medication', 'description']

    class HealthCardVaccinationWriteSerializer(serializers.ModelSerializer):
        class Meta:
            model = HealthCardVaccination
            fields = ['vaccination', 'vaccination_date', 'description']

    class VeterinaryVisitWriteSerializer(serializers.ModelSerializer):
        class Meta:
            model = VeterinaryVisit
            fields = ('doctor', 'date', 'description')

        def validate_date(self, value):
            if value and value > timezone.now().date():
                raise serializers.ValidationError("Date of visit cannot be in the future.")
            return value

    id = serializers.ReadOnlyField()
    animal = serializers.CharField(read_only=True)
    allergies = HealthCardAllergyWriteSerializer(many=True, source='healthcardallergies', required=False)
    medications = HealthCardMedicationWriteSerializer(many=True, source='healthcardmedications', required=False)
    vaccinations = HealthCardVaccinationWriteSerializer(many=True, source='healthcardvaccinations', required=False)
    veterinaryvisits = VeterinaryVisitWriteSerializer(many=True, required=False)

    class Meta:
        model = HealthCard
        fields = ('id', 'animal', 'allergies', 'medications', 'vaccinations', 'veterinaryvisits')

    def update(self, instance, validated_data):
        # # Update HealthCard object

        # Update or create related objects and associate them with the HealthCard
        allergies_data = validated_data.get('healthcardallergies', [])
        medications_data = validated_data.get('healthcardmedications', [])
        vaccinations_data = validated_data.get('healthcardvaccinations', [])
        veterinaryvisits_data = validated_data.get('veterinaryvisits', [])

        # Update or create HealthCardAllergy objects
        for allergy_data in allergies_data:
            allergy, created = HealthCardAllergy.objects.get_or_create(health_card=instance, allergy=allergy_data['allergy'])
            allergy.description = allergy_data.get('description', allergy.description)
            allergy.save()

        # Update or create HealthCardMedication objects
        for medication_data in medications_data:
            medication, created = HealthCardMedication.objects.get_or_create(health_card=instance, medication=medication_data['medication'])
            medication.description = medication_data.get('description', medication.description)
            medication.save()

        # Update or create HealthCardVaccination objects
        for vaccination_data in vaccinations_data:
            vaccination, created = HealthCardVaccination.objects.get_or_create(
                health_card=instance,
                vaccination=vaccination_data['vaccination'],
                vaccination_date=vaccination_data['vaccination_date'])

            vaccination.description = vaccination_data.get('description', vaccination.description)
            vaccination.save()

        # Update or create VeterinaryVisit objects
        for veterinary_visit_data in veterinaryvisits_data:
            veterinary_visit, created = VeterinaryVisit.objects.get_or_create(
                health_card=instance,
                doctor=veterinary_visit_data['doctor'],
                date=veterinary_visit_data['date'],
                description=veterinary_visit_data['description']
            )
            veterinary_visit.doctor = veterinary_visit_data.get('doctor', veterinary_visit.doctor)
            veterinary_visit.date = veterinary_visit_data.get('date', veterinary_visit.date)
            veterinary_visit.description = veterinary_visit_data.get('description', veterinary_visit.description)
            veterinary_visit.save()
        return instance


class HealthCardReadSerializer(serializers.ModelSerializer):
    allergies = HealthCardAllergySerializer(many=True, source='healthcardallergies', required=False)
    medications = HealthCardMedicationSerializer(many=True, source='healthcardmedications', required=False)
    vaccinations = HealthCardVaccinationSerializer(many=True, source='healthcardvaccinations', required=False)
    veterinary_visits = VeterinaryVisitsSerializer(many=True, source='veterinaryvisits', required=False)

    class Meta:
        model = HealthCard
        fields = ('animal', 'allergies', 'medications', 'vaccinations', 'veterinary_visits')


class AnimalReadSerializer(serializers.ModelSerializer):
    added_by = UserSerializer(read_only=True)
    adopted_by = AdopterSerializer(read_only=True)
    health_card = HealthCardReadSerializer(source="healthcards", read_only=True)
    temporary_home = TemporaryHomeSerializer(read_only=True)

    class Meta:
        model = Animal
        fields = [
            "id",
            "name",
            "slug",
            "animal_type",
            "breed",
            "gender",
            "birth_date",
            "description",
            "status",
            "location_where_found",
            "date_when_found",
            "description_of_health",
            "residence",
            "image",
            "temporary_home",

            "added_by",
            "adopted_by",
            "health_card",

            "created_at",
            "updated_at",
        ]
        read_only_fields = ('id', 'slug', 'health_card', 'created_at', 'updated_at')


class AnimalWriteSerializer(AnimalReadSerializer):
    adopted_by = serializers.PrimaryKeyRelatedField(queryset=Adopter.objects.all(), required=False)
    temporary_home = serializers.PrimaryKeyRelatedField(queryset=TemporaryHome.objects.all(), required=False)

    def validate(self, attrs):
        if attrs.get('adopted_by') and attrs.get('status'):
            if attrs.get('status') != "ZAADOPTOWANY":
                raise serializers.ValidationError(_("If there is an adopter, the status must be set ADOPTED or not included"))
            else:
                attrs['status'] = "ADOPTED"
        return attrs

    def update(self, instance, validated_data):
        adopted_by = validated_data.get("adopted_by", None)

        if adopted_by is not None:
            # If adopted_by is provided, update the status to 'ADOPTED'
            instance.status = "ADOPTED"

        return super().update(instance, validated_data)
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
