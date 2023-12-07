from django.urls import path

from reks_manager.user_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    RegistrationFinishView,
    RegistrationLinkView,
    UserDetailsView,
)

app_name = "user_auth"
urlpatterns = [
    path("user/", view=UserDetailsView.as_view(), name="user"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("password/reset/", view=PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/", view=PasswordResetConfirmView.as_view(), name="password_reset_change"),
    # registration
    path("registration/invite/", view=RegistrationLinkView.as_view(), name="registration_invite"),
    path("registration/finish/", view=RegistrationFinishView.as_view(), name="registration_finish"),
]
