from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)

from django.db import models
from django.utils import timezone

from spargo.core.validators import validate_mobile_phone

from model_utils import Choices


class CustomUserManager(UserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        now = timezone.now()
        user = self.model(email=email, is_active=True, is_staff=False,
                          last_login=now, is_superuser=False,
                          date_joined=now, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    email and password are required.
    """
    # Name, email and mobile needs to be case insensitive indexed in postgres
    email = models.EmailField('email address', unique=True, null=True,
                              max_length=254, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    GENDER = Choices(
        (1, 'male', 'Male'),
        (2, 'female', 'Female'),
    )
    gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    mobile_number = models.CharField('Mobile Number', max_length=30, unique=True,
                                     null=True, db_index=True, blank=True,
                                     validators=[validate_mobile_phone])
    gcm_key = models.CharField(blank=True, default='', max_length=254)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __unicode__(self):
        return self.name or self.email or 'User #%d' % (self.id)

    def get_short_name(self):
        return self.email


def cached_auth_preprocessor(user, request):
    if not user.is_authenticated():
        return user
    return user
