from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('This field is required.')

        if not password:
            raise ValueError('This field is required.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png')
    reputation = models.IntegerField(default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.id} - {self.name}"