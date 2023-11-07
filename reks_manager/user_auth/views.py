from allauth.account.models import EmailAddress
from django.contrib.auth import logout as django_logout, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from reks_manager.user_auth.serializers import (
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
    UserDetailsSerializer,
    RegistrationLinkSerializer,
    RegistrationFinishSerializer
)
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import _generate_code, SignupCode

UserModel = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2',
    ),
)


class LogoutView(GenericAPIView):
    """
    Calls Django logout method and deletes the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)
    throttle_scope = 'user_auth'

    def post(self, request, *args, **kwargs):
        """
        Perform logout and delete the Token.
        """
        return self.logout(request)

    def logout(self, request):
        """
        Logout the user and delete the Token.
        """
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        response = Response(
            {'detail': _('Successfully logged out.')},
            status=status.HTTP_200_OK,
        )

        return response


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'user_auth'

    def post(self, request, *args, **kwargs):
        """
        Perform password reset.
        """
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'user_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        """
        Perform password reset confirmation.
        """
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': _('Password changed successfully')},
        )


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    throttle_scope = 'user_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        """
        Perform password change.
        """
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('New password has been saved.')})


class UserDetailsView(RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Get the user object for the request.
        """
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger.
        """
        return UserModel.objects.none()


class RegistrationLinkView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = RegistrationLinkSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = _generate_code()
            try:
                user = get_user_model().objects.get(email=email)
                useremail = EmailAddress.objects.get(user=user, email=email)
                if useremail.verified:
                    content = {'detail': _('Email address already taken.')}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                try:
                    # Delete old signup codes
                    signup_code = SignupCode.objects.get(user=user)
                    signup_code.delete()
                except SignupCode.DoesNotExist:
                    pass

            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(email=email)

            # Set user fields provided
            user.set_password(password)
            user.save()
            emailaddress, _ = EmailAddress.objects.get_or_create(user=user, email=email)
            emailaddress.primary = True
            signup_code = SignupCode.objects.create_signup_code(user)
            signup_code.send_signup_email()

            content = {'email': email}
            return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationFinishView(APIView):
    permission_classes = (AllowAny,)

    def get_serializer(self, *args, **kwargs):
        """
        Get the registration serializer.
         """
        return RegistrationFinishSerializer(*args, **kwargs)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.get_cleaned_data()
        key = cleaned_data.get('key')
        verified = SignupCode.objects.set_user_is_verified(key)

        if verified:
            try:
                signup_code = SignupCode.objects.get(code=key)
                user = signup_code.user
                signup_code.delete()
                email_address = EmailAddress.objects.get(user=user)
                email_address.set_as_primary()
                email_address.set_verified()
                user.first_name = cleaned_data['first_name']
                user.last_name = cleaned_data['last_name']
                user.set_password = cleaned_data['password1']
                user.is_staff = True
                user.save()
            except SignupCode.DoesNotExist:
                pass
            content = {'detail': _('Registriation success.')}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'detail': _('Unable to finish registration.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
