from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class User(models.Model):
  username = models.CharField(max_length=50, unique=True)
  historical = HistoricalRecords()

  def __str__(self):
    return self.username
