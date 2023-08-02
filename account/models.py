from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth. base_user import BaseUserManager
from django.utils.crypto import get_random_string


# Create your models here.
class UserManage(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('Email должен быть обязательно передан')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('У супер юзера должно быть поле is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('У супер юзера должно быть поле is_superuser=True')
        return self._create_user(email, password, **kwargs)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    is_active = models.BooleanField(default=False, help_text="Данное поле служит для активации пользователей")
    phone_number = models.CharField(max_length=25, blank=True, null=True,)

    objects = UserManage()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # def create_activation_code(self):
    #     import uuid
    #     code = str(uuid.uuid4())
    #     self.activation_code = code


    def create_activation_code(self):
        code = get_random_string(6, allowed_chars='123456789')
        self.activation_code = code
        return code
