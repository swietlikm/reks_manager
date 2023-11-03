from django.urls import path, re_path

from reks_manager.user_auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, UserDetailsView, RegistrationLinkView, RegistrationFinishView

app_name = "user_auth"
urlpatterns = [
    path("user/", view=UserDetailsView.as_view(), name="user"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path("password/reset/", view=PasswordResetView.as_view(), name="password_reset"),
    re_path(
        r"^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        view=PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"),
    # registration
    path("registration/invite/", view=RegistrationLinkView.as_view(), name="registration_invite"),
    path("registration/finish/", view=RegistrationFinishView.as_view(), name="registration_finish"),
]
