from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from reks_manager.blog.views import CategoryViewSet, PostViewSet
from reks_manager.core.views import (
    AdopterView,
    AllergyView,
    AnimalPublicView,
    AnimalsPublicViewSet,
    AnimalsViewSet,
    HealthCardView,
    MedicationView,
    TemporaryHomeView,
    VaccinationView,
    VeterinaryVisitView,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("public/animals", AnimalsPublicViewSet)
router.register("public/animal", AnimalPublicView)
router.register("animals", AnimalsViewSet)
router.register("allergy", AllergyView, basename="allergy")
router.register("medication", MedicationView)
router.register("vaccination", VaccinationView)
router.register("veterinary-visit", VeterinaryVisitView)
router.register("temporary-home", TemporaryHomeView)
router.register("adopter", AdopterView)
router.register("health-card", HealthCardView)

router.register("blog/category", CategoryViewSet)
router.register("blog/post", PostViewSet)


app_name = "api"
urlpatterns = router.urls
