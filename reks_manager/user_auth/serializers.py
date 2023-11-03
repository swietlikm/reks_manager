import secrets
import string

from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account.models import EmailAddress
from allauth.account.utils import url_str_to_user_pk as uid_decoder, setup_user_email
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import SignupCode
from .forms import AllAuthPasswordResetForm

UserModel = get_user_model()


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    reset_form = None

    @property
    def password_reset_form_class(self):
        return AllAuthPasswordResetForm

    def validate_email(self, value):
        """
        Validate the email and create PasswordResetForm with the serializer.
        """
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        """
        Save the password reset request.
        """
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
        }

        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset attempt.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    _errors = {}
    user = None
    set_password_form = None

    def validate(self, attrs):
        """
        Validate the password reset confirmation data.
        """
        # Decode the uidb64 (allauth uses base36) to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': [_('Invalid value')]})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': [_('Invalid value')]})

        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        """
        Save the password reset confirmation.
        """
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing the password.
    """
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    set_password_form = None

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = True
        self.logout_on_password_change = True

        super().__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        """
        Validate the old password.
        """
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            err_msg = _('Your old password was entered incorrectly. Please enter it again.')
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        """
        Validate the new password.
        """
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        """
        Save the new password.
        """
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model without password.
    """
    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


class RegistrationLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate_email(self, email):
        """
        Validate the email.
        """
        email = get_adapter().clean_email(email)
        if email and EmailAddress.objects.is_verified(email):
            raise serializers.ValidationError(
                _('A user is already registered with this e-mail address.'),
                )
        return email


class RegistrationFinishSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """
    first_name = serializers.CharField(min_length=2, max_length=255)
    last_name = serializers.CharField(min_length=2, max_length=255)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    key = serializers.CharField(write_only=True)

    def validate_password1(self, password):
        """
        Validate the password.
        """
        return get_adapter().clean_password(password)

    def validate_key(self, key):
        signup_code = SignupCode.objects.filter(code=key).exists()
        if not signup_code:
            raise serializers.ValidationError(_("Invalid registration code"))

    def validate(self, data):
        """
        Validate the registration data.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        """
        Get cleaned data.
        """
        return {
            'key': self.validated_data.get('key', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('first_name', ''),
            'password1': self.validated_data.get('password1', ''),
        }
