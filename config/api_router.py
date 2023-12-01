from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from reks_manager.core.views import AnimalsViewSet, AllergyView, MedicationView, VaccinationView, AnimalsPublicViewSet, VeterinaryVisitView, TemporaryHomeView, AdopterView, HealthCardView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("public/animals", AnimalsPublicViewSet)
router.register("animals", AnimalsViewSet)
router.register("allergy", AllergyView, basename='allergy')
router.register("medication", MedicationView)
router.register("vaccination", VaccinationView)
router.register("veterinary-visit", VeterinaryVisitView)
router.register("temporary-home", TemporaryHomeView)
router.register("adopter", AdopterView)
router.register("health-card", HealthCardView)


app_name = "api"
urlpatterns = router.urls
