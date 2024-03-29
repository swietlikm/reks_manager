from django.views.generic import ListView
from rest_framework import filters
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Adopter, Allergy, Animal, HealthCard, Medication, TemporaryHome, Vaccination, VeterinaryVisit
from .serializers import (
    AdopterSerializer,
    AllergiesSerializer,
    AnimalPublicSerializer,
    AnimalReadSerializer,
    AnimalWriteSerializer,
    HealthCardReadSerializer,
    HealthCardWriteSerializer,
    MedicationsSerializer,
    TemporaryHomeSerializer,
    VaccinationsSerializer,
    VeterinaryVisitsSerializer,
)


class HomeTestView(ListView):
    template_name = "pages/home.html"
    queryset = Animal.objects.filter(status="DO_ADOPCJI")
    context_object_name = "animals"


class BaseAdminAbstractView(ModelViewSet):
    permission_classes = [
        IsAdminUser,
    ]
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
    lookup_field = "health_card"


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


class AnimalsViewSet(ModelViewSet):
    permission_classes = [
        IsAdminUser,
    ]
    queryset = Animal.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AnimalWriteSerializer
        return AnimalReadSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(added_by=self.request.user)
        else:
            serializer.save()


class HealthCardView(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """
    HealthCard CRUD, accepts allergies, vaccinations, medications and veterinaryvisits

    Readonly: created_at, updated_at
    """

    queryset = HealthCard.objects.all()
    lookup_field = "animal"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return HealthCardWriteSerializer
        return HealthCardReadSerializer


#  ------------------------------------------------------------
#  PUBLIC
#  ------------------------------------------------------------


class AnimalsPublicViewSet(ListModelMixin, GenericViewSet):
    """
    PUBLIC ANIMALS SET STATUS = DO_ADOPCJI
    """

    authentication_classes = []
    permission_classes = [
        AllowAny,
    ]
    serializer_class = AnimalPublicSerializer
    queryset = Animal.objects.filter(status="DO_ADOPCJI")
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]


class AnimalPublicView(RetrieveModelMixin, GenericViewSet):
    """
    PUBLIC ANIMAL DATA, STATUS = DO_ADOPCJI
    """

    authentication_classes = []
    permission_classes = [
        AllowAny,
    ]
    serializer_class = AnimalPublicSerializer
    queryset = Animal.objects.filter(status="DO_ADOPCJI")
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]
    lookup_field = "slug"
