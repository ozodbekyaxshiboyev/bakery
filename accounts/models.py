from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from .enums import UserRoles
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .managers import DirectorsManager, VendorsManager, BakersManager, ClientManager, CustomUserManager
from .services import location_image, validate_image, custom_validator
from phonenumber_field import modelfields


class User(AbstractUser):
    phone_number = modelfields.PhoneNumberField(unique=True)
    username = None
    first_name = models.CharField(verbose_name='Name', max_length=50)
    last_name = models.CharField(verbose_name='Surname', max_length=50)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=UserRoles.choices())
    image = models.FileField(upload_to=location_image, validators=[validate_image, custom_validator], blank=True, null=True,
                             help_text='Maximum file size allowed is 2Mb')
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Director(User):
    objects = DirectorsManager()

    class Meta:
        proxy = True


class Baker(User):
    objects = BakersManager()

    class Meta:
        proxy = True


class Vendor(User):
    objects = VendorsManager()

    class Meta:
        proxy = True


class Client(User):
    objects = ClientManager()

    class Meta:
        proxy = True

