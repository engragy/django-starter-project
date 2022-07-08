import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def overwrite_file(desired_name, filename):
    '''function to overrite file if it already exists'''
    uploaded_file_ext = filename.split('.')[-1]
    filename = f"{desired_name}.{uploaded_file_ext}"
    relativepath = os.path.join('users_pics', filename)
    fullpath = os.path.join(settings.MEDIA_ROOT, relativepath)
    if os.path.exists(fullpath):
        os.remove(fullpath)
    return filename


def upload_user_image(instance, filename):
    '''function avatar media naming scheme, returns "users/{instance.user}/{filename}"'''
    desired_name = f'pic_{instance.first_name}_{instance.last_name}'
    newname = overwrite_file(desired_name, filename)
    return os.path.join('users_pics', newname)


class CustomUser(AbstractUser):
    GENDER_CHOICES = ((0, 'FEMALE'), (1, 'MALE'))
    PHONE_REGEX = RegexValidator(
        regex=r'^\+2\d{9,15}$',
        message="Phone number must be entered in the format: '+xxxxxxxxxxxxxxx'. Up to 10 digits allowed."
    )

    first_name = models.CharField(_('First Name'), max_length=64)
    last_name = models.CharField(_('Last Name'), max_length=64)
    country_code = models.CharField(_('Country Code'), max_length=2)
    phone_number = models.CharField(
        _('Phone Number'), validators=[PHONE_REGEX, MinLengthValidator(10)], max_length=12, unique=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=1)
    birthdate = models.DateField(_('Date of Birth'))
    avatar = models.ImageField(
        upload_to=upload_user_image,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'],)])
    email = models.EmailField(_('E-mail'), blank=True, null=True, unique=True)

    # required fields during adding superuser
    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'country_code', 'phone_number', 'gender', 'birthdate'
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomUserStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(_('Phone Number'), validators=[CustomUser.PHONE_REGEX], max_length=12, unique=True)
    auth_token = models.CharField(_('Auth-Token'), max_length=64)
    status = models.JSONField(_('Status'))
