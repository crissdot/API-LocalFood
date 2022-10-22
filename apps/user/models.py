from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from simple_history.models import HistoricalRecords

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
  is_superuser = models.BooleanField(default=False)
  objects = UserManager()
  historical = HistoricalRecords()

  @property
  def _history_user(self):
    return self.changed_by

  @_history_user.setter
  def _history_user(self, value):
    self.changed_by = value

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
