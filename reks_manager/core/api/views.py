from rest_framework import filters
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin
from .serializers import AnimalSerializer, HealthCardSerializer


from reks_manager.core.models import Animal, HealthCard


class AnimalsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "slug", "animal_type", "status"]
    ordering_fields = ["name", "animal_type", "status", "birth_date"]


class AnimalViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()
    lookup_field = "pk"


class HealthCardViewSet(ModelViewSet):
    queryset = HealthCard.objects.all()
    serializer_class = HealthCardSerializer
