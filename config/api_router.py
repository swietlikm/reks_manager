from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from reks_manager.core.views import AnimalsViewSet, AnimalViewSet, AllergyView, MedicationView, VaccinationView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("animals", AnimalsViewSet)
router.register("animal", AnimalViewSet)
router.register("allergy", AllergyView)
router.register("medication", MedicationView)
router.register("vaccination", VaccinationView)


app_name = "api"
urlpatterns = router.urls
