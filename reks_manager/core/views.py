from rest_framework import filters
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Animal, HealthCard, Allergy, Medication, Vaccination, VeterinaryVisit, TemporaryHome, Adopter
from .serializers import AnimalSerializer, HealthCardSerializer, AllergiesSerializer, MedicationsSerializer, VaccinationsSerializer, AnimalPublicSerializer, VeterinaryVisitsSerializer, TemporaryHomeSerializer, AdopterSerializer


class BaseAdminAbstractView(ModelViewSet):
    permission_classes = [IsAdminUser,]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "name"]
    ordering_fields = ["id", "name"]


class AllergyView(BaseAdminAbstractView):
    """
    Allergy CRUD, accepts name, category, description

    Readonly: created_at, updated_at
    """
    queryset = Allergy.objects.all()
    serializer_class = AllergiesSerializer
    search_fields = ["name", "category"]
    ordering_fields = ["name", "category"]


class MedicationView(BaseAdminAbstractView):
    """
    Medication CRUD, accepts name, description

    Readonly: created_at, updated_at
    """
    queryset = Medication.objects.all()
    serializer_class = MedicationsSerializer


class VaccinationView(BaseAdminAbstractView):
    """
    Vaccination CRUD, accepts name, description

    Readonly: created_at, updated_at
    """
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationsSerializer


class VeterinaryVisitView(BaseAdminAbstractView):
    """
    VeterinaryVisit CRUD, accepts health_card, doctor choice, date, description

    Readonly: created_at, updated_at
    """
    queryset = VeterinaryVisit.objects.all()
    serializer_class = VeterinaryVisitsSerializer
    search_fields = ["health_card", "doctor", "date"]
    ordering_fields = ["health_card", "doctor", "date"]


class TemporaryHomeView(BaseAdminAbstractView):
    """
    TemporaryHome CRUD, accepts owner, phone_number, city, street, building, apartment, zip_code

    Readonly: created_at, updated_at
    """
    queryset = TemporaryHome.objects.all()
    serializer_class = TemporaryHomeSerializer
    search_fields = ["owner", "phone_number", "city", "street", "zip_code"]
    ordering_fields = ["owner", "city", "street", "zip_code"]


class AdopterView(BaseAdminAbstractView):
    """
    TemporaryHome CRUD, accepts owner, phone_number, address

    Readonly: created_at, updated_at
    """
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    search_fields = ["owner", "phone_number", "address"]
    ordering_fields = ["owner", "address"]


class AnimalsViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAdminUser,]
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]


class AnimalViewSet(RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAdminUser,]
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    lookup_field = "pk"


class HealthCardViewSet(ModelViewSet):
    queryset = HealthCard.objects.all()
    serializer_class = HealthCardSerializer

#  ------------------------------------------------------------
#  PUBLIC
#  ------------------------------------------------------------


class AnimalsPublicViewSet(ListModelMixin, GenericViewSet):
    """
    PUBLIC ANIMALS SET STATUS = DO_ADOPCJI
    """
    authentication_classes = []
    permission_classes = [AllowAny,]
    serializer_class = AnimalPublicSerializer
    queryset = Animal.objects.filter(status="DO_ADOPCJI")
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]

