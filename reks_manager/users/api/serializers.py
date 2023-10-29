from django.contrib.auth import get_user_model
from rest_framework import serializers

from reks_manager.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        # fields = ["first_name", "last_name", "url"]
        #
        # extra_kwargs = {
        #     "url": {"view_name": "dj-rest-auth:rest_user_details", "lookup_field": "pk"},
        # }
