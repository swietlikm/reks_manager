from rest_framework import filters
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Animal, HealthCard, Allergy, Medication, Vaccination
from .serializers import AnimalSerializer, HealthCardSerializer, AllergiesSerializer, MedicationsSerializer, VaccinationsSerializer


class BaseAdminAbstractView(ModelViewSet):
    permission_classes = [IsAdminUser,]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]


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


class AnimalsViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = [IsAdminUser,]
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]


class AnimalViewSet(RetrieveModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    lookup_field = "pk"


class HealthCardViewSet(ModelViewSet):
    queryset = HealthCard.objects.all()
    serializer_class = HealthCardSerializer
