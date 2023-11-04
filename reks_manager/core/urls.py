from django.urls import path

from .views import AnimalViewSet, AnimalsViewSet

app_name = "core"

urlpatterns = [
    path("animals/", view=AnimalViewSet.as_view(), name="animals"),
    path("animals/<id:pk>", view=AnimalsViewSet.as_view(), name="animal"),
]
