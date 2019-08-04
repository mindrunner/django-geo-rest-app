from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.contrib.gis.db import models


class ProviderUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class Provider(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, unique=True)
    phone = models.CharField(max_length=256)
    language = models.CharField(max_length=256)
    currency = models.CharField(max_length=256)
    is_staff = models.BooleanField(default=False)

    objects = ProviderUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"

    def __unicode__(self):
        return self.name


class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    polygon = models.PolygonField(srid=4326, default=None)

    class Meta:
        verbose_name = "Service Area"
        verbose_name_plural = "Service Areas"

    def __unicode__(self):
        return self.name
