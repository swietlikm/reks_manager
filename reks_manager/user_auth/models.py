import binascii
import os
import secrets
import string

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail, EmailMultiAlternatives

EXPIRY_PERIOD = 3  # days

User = get_user_model()


def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode('utf-8')
#
#
# def _generate_password(self, length=12):
#     """
#     Generate a random password.
#     """
#     alphabet = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(secrets.choice(alphabet) for _ in range(length))


class SignupCodeManager(models.Manager):
    def create_signup_code(self, user):
        code = _generate_code()
        signup_code = self.create(user=user, code=code)

        return signup_code

    def set_user_is_verified(self, code):
        try:
            signup_code = SignupCode.objects.get(code=code)
            signup_code.user.is_verified = True
            signup_code.user.save()
            return True
        except SignupCode.DoesNotExist:
            pass

        return False


def send_multi_format_email(template_prefix, template_ctxt, target_email):
    subject_file = 'email/%s_subject.txt' % template_prefix
    txt_file = 'email/%s.txt' % template_prefix
    html_file = 'email/%s.html' % template_prefix

    subject = render_to_string(subject_file).strip()
    from_email = settings.DEFAULT_FROM_EMAIL
    to = target_email
    # bcc_email = settings.EMAIL_BCC
    text_content = render_to_string(txt_file, template_ctxt)
    html_content = render_to_string(html_file, template_ctxt)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to],)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


class SignupCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(_('code'), max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SignupCodeManager()

    def send_signup_email(self):
        prefix = 'signup_email'
        self.send_email(prefix)

    def send_email(self, prefix):
        ctxt = {
            'email': self.user.email,
            'code': self.code
        }
        send_multi_format_email(prefix, ctxt, target_email=self.user.email)

    def __str__(self):
        return self.code
