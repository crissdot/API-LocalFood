from email.policy import default
from django.db import models
from simple_history.models import HistoricalRecords

from ..base.models import BaseModel

# Create your models here.
class LocalFood(BaseModel):
  SOCIAL_MEDIAS_OPTIONS = (
    ('WA', 'Whatsapp'),
    ('FB', 'Facebook'),
    ('TW', 'Twitter'),
    ('IG', 'Instagram'),
  )

  name = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  address = models.CharField(max_length=100, null=True, blank=True)
  phone_number = models.CharField(max_length=10, null=True, blank=True)
  schedule = models.CharField(max_length=100, null=True, blank=True)
  has_delivery = models.BooleanField(default=False)
  social_medias = models.CharField(max_length=2, choices=SOCIAL_MEDIAS_OPTIONS, null=True, blank=True)
  profile_image = models.ImageField(upload_to='images/localfood/', null=True, blank=True)
  banner_image = models.ImageField(upload_to='images/localfood/', null=True, blank=True)
  historical = HistoricalRecords()

  @property
  def _history_user(self):
    return self.changed_by

  @_history_user.setter
  def _history_user(self, value):
    self.changed_by = value

  def __str__(self):
    return f'{self.name}: {self.description}'

  class Meta:
    verbose_name='Local Food (Negocio)'
    verbose_name_plural='Local Foods (Negocios)'
