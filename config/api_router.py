from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from reks_manager.users.api.views import UserViewSet
from reks_manager.core.api.views import AnimalsViewSet, AnimalViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("animals", AnimalsViewSet)
router.register("animal", AnimalViewSet)


app_name = "api"
urlpatterns = router.urls
