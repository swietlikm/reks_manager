from reks_manager.core.models import Animal, HealthCard
from rest_framework import filters
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .serializers import AnimalSerializer, HealthCardSerializer


class AnimalsViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]


class AnimalViewSet(RetrieveModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    lookup_field = "pk"


class HealthCardViewSet(ModelViewSet):
    queryset = HealthCard.objects.all()
    serializer_class = HealthCardSerializer
