from django.db import models
from .enums import UserRoles
from django.contrib.auth.models import BaseUserManager
from django.contrib import auth
from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, first_name, last_name, email, password, **extra_fields):
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, phone_number, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, first_name, last_name, email, password, **extra_fields)


class DirectorsManager(BaseUserManager):
    def get_queryset(self):
        return super(DirectorsManager, self).get_queryset().filter(
            role=UserRoles.director.value)

    def create(self, **kwargs):
        kwargs.update({'role': UserRoles.director.value})
        return super(DirectorsManager, self).create(**kwargs)


class VendorsManager(models.Manager):
    def get_queryset(self):
        return super(VendorsManager, self).get_queryset().filter(
            role=UserRoles.manager.value)

    def create(self, **kwargs):
        kwargs.update({'role': UserRoles.manager.value})
        return super(VendorsManager, self).create(**kwargs)


class BakersManager(models.Manager):
    def get_queryset(self):
        return super(BakersManager, self).get_queryset().filter(
            role=UserRoles.teacher.value)

    def create(self, **kwargs):
        kwargs.update({'role': UserRoles.teacher.value})
        return super(BakersManager, self).create(**kwargs)



class ClientManager(models.Manager):
    def get_queryset(self):
        return super(ClientManager, self).get_queryset().filter(
            role=UserRoles.student.value)

    def create(self, **kwargs):
        kwargs.update({'role': UserRoles.student.value})
        return super(ClientManager, self).create(**kwargs)