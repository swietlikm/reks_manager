from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from reks_manager.users.managers import UserManager  # noqa


class User(AbstractUser):
    """
    Default custom user model for reks_manager.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    first_name = CharField(_("First name"),max_length=255)
    last_name = CharField(_("Last name"),max_length=255)
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
