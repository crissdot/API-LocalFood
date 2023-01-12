from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from ..base.models import BaseModel

# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, username, password=None):
    if not username:
      raise ValueError('The user needs a username')

    user = self.model(username=username)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, username, password=None):
    user = self.create_user(username, password)
    user.is_superuser = True
    user.save()
    return user

class User(AbstractBaseUser, BaseModel):
  username = models.CharField(max_length=50, unique=True)
  name = models.CharField(max_length=50, null=True, blank=True)
  last_name = models.CharField(max_length=50, null=True, blank=True)
  phone_number = models.CharField(max_length=10, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  is_superuser = models.BooleanField(default=False)
  profile_image = models.ImageField(upload_to='images/user/', null=True, blank=True)
  objects = UserManager()

  USERNAME_FIELD = 'username'
  # REQUIRED_FIELDS = []

  def has_perm(self, perm, obj=None):
    return self.is_superuser

  def has_module_perms(self, app_label):
    return self.is_superuser

  @property
  def is_staff(self):
    return self.is_superuser

  def __str__(self):
    return self.username
