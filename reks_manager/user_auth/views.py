from allauth.account import app_settings as allauth_account_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
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
    RegisterLinkSerializer,
    RegisterSerializer,
)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

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
    serializer_class = None
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
            {'detail': _('Password has been reset with the new password.')},
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


class RegisterLinkView(CreateAPIView):
    """
    Create a user with a registration link.
    """
    serializer_class = RegisterLinkSerializer
    permission_classes = (IsAdminUser,)
    token_model = Token
    throttle_scope = 'auth_user'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        """
        Perform user registration via a link.
        """
        return super().dispatch(*args, **kwargs)

    def get_response_data(self, user):
        """
        Get the registration response data.
        """
        return {'detail': _('Registration e-mail sent.')}

    def create(self, request, *args, **kwargs):
        """
        Create a new user with a registration link.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Check if a user with the given email address already exists
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            user = None

        if user:
            # Check if the user's email is not verified, then send a verification email
            email_address = EmailAddress.objects.get(user=user, email=email)
            if not email_address.verified:
                email_address.send_confirmation(request)
                return Response({'detail': _('Verification e-mail sent.')}, status=status.HTTP_200_OK)

        if user is None:
            # If the user doesn't exist, proceed with user creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        response = Response(data, status=status.HTTP_201_CREATED, headers=headers)
        return response

    def perform_create(self, serializer):
        """
        Perform user creation with a registration link.
        """
        user = serializer.save(self.request)
        complete_signup(
            self.request._request, user,
            allauth_account_settings.EMAIL_VERIFICATION,
            None,
        )
        return user


class RegistrationView(APIView, ConfirmEmailView):
    """
    Handle user registration via email confirmation.
    """
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        """
        Dispatch user registration view.
        """
        return super().dispatch(*args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        """
        Get the registration serializer.
        """
        return RegisterSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Handle GET method, not allowed.
        """
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        """
        Handle user registration via email confirmation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.get_cleaned_data()
        self.kwargs['key'] = cleaned_data['key']
        confirmation = self.get_object()
        user = confirmation.email_address.user

        user.first_name = cleaned_data['first_name']
        user.last_name = cleaned_data['last_name']
        user.set_password = cleaned_data['password1']
        user.is_staff = True
        user.save()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)
